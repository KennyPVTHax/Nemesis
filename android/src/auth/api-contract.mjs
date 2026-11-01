/** Exact deployed response structure supplied by the owner on 2026-10-30.
 * /auth/me has no separate numeric/user ID; its login_id is the canonical identity.
 * Account expires_at (nullable UNIX seconds) is independent of token expires_in.
 */
export const LIVE_AUTH_CONTRACT=Object.freeze({
 confirmed:true,
 provenance:'Owner-verified deployed backend success JSON, 2026-10-30.',
 tokenPath:'access_token',tokenTypePath:'token_type',tokenTtlPath:'expires_in',
 profilePath:'$',idPath:'login_id',loginPath:'login_id',rolePath:'role',
 activePath:'is_active',accountExpiryPath:'expires_at',accountExpiryFormat:'unix-seconds',
 sessionExpiryPath:null,sessionExpiryFormat:null,
 challengeExpiryPath:null,challengeExpiryFormat:null,
 challengeTtlPath:'expires_in',
});
