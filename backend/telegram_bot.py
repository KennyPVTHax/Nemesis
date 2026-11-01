import os
import time
from pathlib import Path

import httpx

from telegram_link import consume_code, is_owner
from registration_store import new_key, redeem, setid, status as registration_status, setup as registration_setup

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}/"

OFFSET_FILE = Path("/opt/nemesis/data/telegram.offset")


class TelegramDeliveryForbidden(RuntimeError):
    pass


def api(client, method, payload=None):
    response = client.post(API + method, json=payload or {})
    if response.status_code == 403 and method == "sendMessage":
        try:
            description = str(
                response.json().get("description", "")
            ).lower()
        except ValueError:
            description = ""

        if "blocked" in description:
            reason = "bot_blocked"
        elif "initiate" in description:
            reason = "conversation_not_started"
        elif "deactivated" in description:
            reason = "user_deactivated"
        elif "kicked" in description:
            reason = "bot_removed"
        else:
            reason = "forbidden"

        raise TelegramDeliveryForbidden(
            "Telegram sendMessage HTTP 403 (" + reason + ")"
        )

    if response.status_code != 200:
        reason = "api_error"

        if response.status_code == 409:
            try:
                description = str(
                    response.json().get("description", "")
                ).lower()
            except ValueError:
                description = ""

            reason = (
                "webhook_conflict"
                if "webhook" in description
                else "another_poller_conflict"
            )

        raise RuntimeError(
            f"Telegram {method} HTTP "
            f"{response.status_code} ({reason})"
        )

    data = response.json()

    if not data.get("ok"):
        raise RuntimeError("Telegram API operation failed")

    return data["result"]


def send(client, chat_id, text):
    return api(client, "sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True,
    })


def process(client, username, update):
    from firebase_telegram import Manager,handle
    manager=Manager(lambda chat,text,keyboard=None:api(client,'sendMessage',{'chat_id':chat,'text':text,'disable_web_page_preview':True,**({'reply_markup':keyboard} if keyboard else {})}))
    if handle(update,username,manager,lambda q,text:api(client,'answerCallbackQuery',{'callback_query_id':q,'text':text})):
        return
    message = update.get("message")

    if not isinstance(message, dict):
        return

    print("Telegram message received", flush=True)

    chat = message.get("chat") or {}
    sender = message.get("from") or {}

    if chat.get("type") != "private":
        return

    chat_id = chat.get("id")

    if not isinstance(chat_id, int) or sender.get("id") != chat_id:
        return

    text = message.get("text")

    if not isinstance(text, str):
        return

    parts = text.strip().split(maxsplit=1)

    if not parts:
        return

    raw_command = parts[0].lower()
    command, _, target = raw_command.partition("@")

    if target and target != username.lower():
        return

    if command in ("/start", "/help"):
        send(
            client,
            chat_id,
            "NEMESIS Authentication Bot\n\n"
            "Commands:\n"
            "/start — Welcome\n"
            "/help — Available commands\n"
            "/status — Check account linking\n"
            "/link CODE — Link owner account\n\n"
            "/newkey, /redeem KEY, /setid NAME, /registration, /setup, /cancel\n"
            "Owner Firebase Manager: /firebase"
        )

    elif command == "/status":
        if is_owner(chat_id):
            send(
                client, chat_id,
                "NEMESIS Owner\n"
                "Login ID: NemesisOwner\n"
                "Telegram linked: Yes\n"
                "Access: Unlimited"
            )
        else:
            send(
                client, chat_id,
                "No NEMESIS account is linked "
                "to this Telegram account yet."
            )

    elif command == "/newkey":
        send(client, chat_id, new_key(chat_id))
    elif command == "/redeem":
        send(client, chat_id, redeem(chat_id, parts[1].strip() if len(parts)==2 else ""))
    elif command == "/setid":
        send(client, chat_id, setid(chat_id, parts[1].strip() if len(parts)==2 else ""))
    elif command == "/registration":
        send(client, chat_id, registration_status(chat_id))
    elif command == "/setup":
        send(client, chat_id, registration_setup(chat_id, "https://nemesispanel.shop"))
    elif command == "/cancel":
        from account_store import connect
        with connect() as db:
            db.execute("DELETE FROM registrations WHERE chat_id=?", (chat_id,))
            db.execute("DELETE FROM signup_tokens WHERE chat_id=?", (chat_id,))
        send(client, chat_id, "Pending registration cancelled.")

    elif command == "/link":
        if len(parts) != 2:
            send(client, chat_id, "Use /link CODE")
            return

        result = consume_code(chat_id, parts[1].strip())

        messages = {
            "linked": (
                "NEMESIS OWNER LINKED SUCCESSFULLY.\n\n"
                "Login ID: NemesisOwner\n"
                "Telegram authentication: Connected\n"
                "Access: Unlimited"
            ),
            "already": "Your Telegram account is already linked.",
            "invalid": "Invalid linking code.",
            "expired": "Linking code expired or locked. Generate a new code.",
            "unavailable": "Owner linking is unavailable.",
        }

        send(client, chat_id, messages.get(result, "Linking failed."))


def load_offset():
    try:
        return max(0, int(OFFSET_FILE.read_text().strip()))
    except FileNotFoundError:
        return 0


def save_offset(value):
    temp = OFFSET_FILE.with_name(
        OFFSET_FILE.name + f".{os.getpid()}.tmp"
    )
    temp.write_text(str(value))
    os.chmod(temp, 0o600)
    os.replace(temp, OFFSET_FILE)


def main():
    os.umask(0o077)
    from firebase_pool import init
    init()
    with httpx.Client(
        timeout=httpx.Timeout(30.0, connect=10.0)
    ) as client:
        me = api(client, "getMe")
        username = me["username"]

        webhook = api(client, "getWebhookInfo")

        if webhook.get("url"):
            raise RuntimeError(
                "A webhook exists; polling cannot start"
            )

        print(
            f"NEMESIS Telegram bot started: @{username}",
            flush=True
        )

        from firebase_telegram import Manager
        from firebase_worker import loop
        import threading
        worker_manager=Manager(lambda chat,text,keyboard=None:api(client,'sendMessage',{'chat_id':chat,'text':text,'disable_web_page_preview':True,**({'reply_markup':keyboard} if keyboard else {})}))
        stop=threading.Event()
        threading.Thread(target=loop,args=(worker_manager,stop),daemon=True).start()
        offset = load_offset()

        while True:
            try:
                updates = api(client, "getUpdates", {
                    "offset": offset,
                    "timeout": 15,
                    "limit": 20,
                    "allowed_updates": ["message", "callback_query"],
                })

                from firebase_manager_store import transaction
                with transaction() as db:db.execute('INSERT OR REPLACE INTO firebase_manager_health VALUES(1,?)',(int(time.time()),))
                for update in updates:
                    try:
                        process(client, username, update)
                    except TelegramDeliveryForbidden as exc:
                        print(
                            "Undeliverable Telegram reply:",
                            str(exc),
                            "- skipping affected update",
                            flush=True,
                        )

                    except Exception:
                        print("Telegram update failed; update isolated",flush=True)
                    offset = update["update_id"] + 1
                    save_offset(offset)

            except Exception as exc:
                # Never print request URLs containing the token.
                print(
                    "Telegram polling error:",
                    (
                        str(exc)
                        if isinstance(exc, RuntimeError)
                        and str(exc).startswith("Telegram ")
                        else type(exc).__name__
                    ),
                    flush=True
                )
                time.sleep(3)


if __name__ == "__main__":
    main()
