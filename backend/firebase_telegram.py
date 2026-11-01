"""Private linked-owner manager, opaque single-use inline actions and guided input."""
import json,time
from account_store import connect
import firebase_config as cfg
import firebase_manager_store as store
import firebase_jobs as jobs
MENU=[('Add Firebase','add'),('Create Firebase','create'),('View Pool','pool'),('Customer Assignments','assignments'),('Pending Requests','requests'),('Test Connectivity','test'),('Disable Instance','disable'),('Audit History','audit'),('Provisioning Jobs','jobs')]

class Manager:
    def __init__(self,send):self.send=send
    def message(self,chat,text,buttons=()):
        tokens=[];keyboard=[]
        for caption,kind,payload in buttons:
            token=store.action(chat,kind,payload);tokens.append(token)
            button={'text':caption,'callback_data':token}
            if keyboard and len(keyboard[-1])==1:keyboard[-1].append(button)
            else:keyboard.append([button])
        result=self.send(chat,text,{'inline_keyboard':keyboard} if keyboard else None)
        if tokens:
            if not result or not isinstance(result.get('message_id'),int):raise cfg.ManagerError('telegram_message_not_confirmed')
            store.bind(chat,result['message_id'],tokens)
    def aliases(self,chat,payload):
        self.message(chat,'Select an authorized server-side project alias. No credential files or keys are accepted here.',[(alias,'profile',{**payload,'alias':alias}) for alias in cfg.profiles()])
    def confirm(self,chat,text,op,payload):self.message(chat,text,[('Confirm','confirm',{'op':op,**payload}),('Cancel','menu',{'section':'home'})])
    def show(self,chat,section='home',page=0):
        if section=='home':
            recent=store.rows('audit')[:3]
            return self.message(chat,'Firebase Manager\n'+store.overview()+'\nRecent: '+str(recent),[(a,'menu',{'section':b}) for a,b in MENU])
        if section=='add':
            store.wizard(chat,'add_label',{});return self.message(chat,'Send a unique database label. Use /cancel to cancel.')
        if section=='create':return self.aliases(chat,{'kind':'create'})
        rows=store.rows('pool' if section in ('disable','test') else section,page)
        buttons=[]
        if section=='requests':
            for login,uid,revision in rows:
                for accept in (True,False):buttons.append((('Approve ' if accept else 'Deny ')+login,'decision_prompt',{'user_id':uid,'revision':revision,'approve':accept}))
        if section in ('disable','test'):
            for label,*_ in rows:buttons.append((label,'instance',{'kind':section,'label':label}))
        if len(rows)==8 and page<125:buttons.append(('Next','menu',{'section':section,'page':page+1}))
        if page:buttons.append(('Previous','menu',{'section':section,'page':page-1}))
        buttons.append(('Manager','menu',{'section':'home'}))
        return self.message(chat,section.title()+'\n'+('\n'.join(' | '.join(map(str,r)) for r in rows) or 'No records.'),buttons)
    def instance(self,label):
        with connect() as db:r=db.execute('SELECT i.database_url,m.alias,u.login_id FROM firebase_instances i JOIN firebase_manager_instances m ON m.instance_id=i.id LEFT JOIN users u ON u.id=i.assigned_user_id WHERE i.label=?',(label,)).fetchone()
        if not r:raise cfg.ManagerError('unknown_instance')
        return r
    def command(self,chat,text):
        parts=text.split();cmd=parts[0].split('@')[0];args=parts[1:]
        with store.transaction() as db:store.owner(db,chat);store.throttle(db,chat)
        if cmd=='/firebase':return self.show(chat)
        section={'/firebase_add':'add','/firebase_create':'create','/firebase_list':'pool','/firebase_requests':'requests','/firebase_audit':'audit'}.get(cmd)
        if section:return self.show(chat,section)
        if cmd=='/firebase_assign' and len(args)==2:return self.confirm(chat,'Confirm permanent dedicated assignment; no existing assignment will be replaced.','assign',{'label':cfg.label(args[0]),'login':args[1]})
        if cmd in ('/firebase_test','/firebase_enable','/firebase_disable') and 1<=len(args)<=2:return self.instance_prompt(chat,cmd.removeprefix('/firebase_'),args[0],args[1] if len(args)==2 else None)
        if cmd in ('/firebase_approve','/firebase_deny') and len(args)==1:
            with connect() as db:r=db.execute("SELECT r.user_id,v.revision FROM firebase_link_requests r JOIN users u ON u.id=r.user_id JOIN firebase_manager_request_versions v ON v.user_id=r.user_id WHERE u.login_id=? AND r.state='pending'",(args[0],)).fetchone()
            if not r:raise cfg.ManagerError('request_no_longer_pending')
            return self.confirm(chat,'Confirm link disclosure decision for '+args[0],'decision',{'user_id':r[0],'revision':r[1],'approve':cmd=='/firebase_approve'})
        return self.message(chat,'Usage: /firebase_assign LABEL LOGIN; /firebase_test LABEL [ALIAS]; /firebase_disable LABEL; /firebase_enable LABEL [ALIAS]; /firebase_approve LOGIN; /firebase_deny LOGIN. Or open /firebase.')
    def instance_prompt(self,chat,kind,label,alias=None):
        url,stored,customer=self.instance(label)
        if kind=='disable':return self.confirm(chat,'Disable '+label+'? Affected customer: '+str(customer or 'none')+'. Access through this backend will pause; assignment and database data are retained.','disable',{'label':label,'expected_customer':customer})
        alias=alias or stored
        payload={'kind':kind,'label':label,'url':url}
        if not alias:return self.aliases(chat,payload)
        cfg.profile(alias)
        return self.confirm(chat,'Verify '+label+' with '+alias+'? Failed checks will block access until verified again.',kind,{'label':label,'url':url,'alias':alias})
    def text(self,chat,text):
        wizard=store.take_wizard(chat)
        if not wizard:return False
        if len(text)>250 or 'private_key' in text.lower() or '-----BEGIN' in text:raise cfg.ManagerError('credentials_must_not_be_sent_to_telegram')
        stage,payload=wizard
        if stage=='add_label':
            payload['label']=cfg.label(text);store.wizard(chat,'add_url',payload);self.message(chat,'Send the exact HTTPS Realtime Database URL.')
        elif stage=='add_url':
            payload['url']=cfg.identity(text)[0];store.clear_wizard(chat);self.aliases(chat,{'kind':'inspect',**payload})
        elif stage=='create_label':
            payload['label']=cfg.label(text);store.clear_wizard(chat)
            self.confirm(chat,'Create a billed dedicated database in '+payload['alias']+'? Deny-all direct-client Rules will be applied. Project quota and configured resource caps must pass.','create',payload)
        return True
    def callback(self,chat,message_id,data):
        kind,p=store.consume(chat,message_id,data)
        if kind=='menu':return self.show(chat,p.get('section','home'),int(p.get('page',0)))
        if kind=='profile':
            cfg.profile(p['alias'])
            if p['kind']=='create':
                store.wizard(chat,'create_label',{'alias':p['alias']});return self.message(chat,'Send the new database label. Region: '+cfg.profile(p['alias'])['region'])
            if p['kind']=='inspect':
                jid=jobs.enqueue_job(chat,'inspect',p['label'],p['alias'],p['url']);return self.message(chat,'Validation queued: '+jid+'. Registration requires a separate confirmation after checks pass.')
            return self.instance_prompt(chat,p['kind'],p['label'],p['alias'])
        if kind=='instance':return self.instance_prompt(chat,p['kind'],p['label'])
        if kind=='decision_prompt':return self.confirm(chat,'Confirm '+('approval' if p['approve'] else 'denial')+' of the pending customer link request?','decision',p)
        if kind=='confirm':
            op=p['op']
            if op=='register':iid=jobs.register(chat,p['job_id'],p['result_hash']);return self.message(chat,'Database registered and validated. Instance record: '+str(iid))
            if op=='decision':return self.message(chat,'Request '+store.decision(chat,p['user_id'],p['revision'],p['approve'])+'.')
            if op=='disable':store.disable(chat,p['label'],p['expected_customer']);return self.message(chat,'Instance disabled; assignment and data retained.')
            if op=='assign':return self.message(chat,store.manual_assign(chat,p['label'],p['login']))
            if op in ('create','test','enable'):
                jid=jobs.enqueue_job(chat,op,p['label'],p['alias'],p.get('url'));return self.message(chat,'Operation queued: '+jid+'. No success is claimed until cloud and isolation verification finish.')
        raise cfg.ManagerError('invalid_callback')

def private(message,sender=None,bot_username=None):
    if not isinstance(message,dict):return None
    chat=message.get('chat',{});sender=sender or message.get('from',{})
    if chat.get('type')!='private' or not isinstance(sender.get('id'),int) or chat.get('id')!=sender['id']:return None
    if any(message.get(k) for k in ('forward_origin','forward_date','forward_from','is_automatic_forward')):return None
    if bot_username:
        author=message.get('from',{})
        if author.get('is_bot') is not True or author.get('username','').casefold()!=bot_username.casefold():return None
    return chat['id']

def handle(update,username,manager,answer):
    callback=update.get('callback_query')
    message=update.get('message')
    if callback:
        chat=private(callback.get('message'),callback.get('from'),username)
        try:
            if chat is None:raise cfg.ManagerError('private_owner_conversation_required')
            if not cfg.enabled():raise cfg.ManagerError('firebase_manager_disabled')
            manager.callback(chat,callback['message']['message_id'],callback.get('data'))
            answer(callback['id'],'Processed')
        except Exception:
            answer(callback.get('id'),'Action unavailable or expired. Reopen /firebase.')
        return True
    if not isinstance(message,dict):return False
    text=message.get('text','');cmd=text.split(maxsplit=1)[0] if text.strip() else ''
    targeted=cmd.partition('@')[2]
    if targeted and targeted.casefold()!=username.casefold():return False
    is_command=cmd.split('@')[0].startswith('/firebase')
    chat=private(message)
    if is_command and chat is None:return True
    if chat is None:return False
    try:
        if is_command:
            with store.transaction() as db:store.owner(db,chat)
            if not cfg.enabled():manager.message(chat,'Firebase Manager is disabled pending secure server configuration.');return True
            if not store.seen(update.get('update_id',message.get('message_id',0))):return True
            manager.command(chat,text);return True
        if text=='/cancel':
            with connect() as db:
                if db.execute("SELECT 1 FROM users WHERE role='owner' AND is_active=1 AND telegram_chat_id=?",(chat,)).fetchone():store.clear_wizard(chat)
            return False
        if not text.startswith('/') and cfg.enabled():
            with connect() as db:
                if not db.execute("SELECT 1 FROM users WHERE role='owner' AND is_active=1 AND telegram_chat_id=? AND login_id='NemesisOwner' COLLATE NOCASE",(chat,)).fetchone():return False
            return manager.text(chat,text)
    except cfg.ManagerError as e:
        # Diagnostic codes only; no raw exception details or customer messages.
        if is_command or cfg.enabled():manager.send(chat,'Firebase action unavailable. Check owner authorization/configuration or reopen /firebase.',None)
        return is_command or bool(cfg.enabled())
    except Exception:
        manager.send(chat,'Firebase operation could not be completed. Reopen /firebase.',None);return True
    return False
