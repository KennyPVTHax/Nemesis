/** Only owner-confirmed response paths belong here. Never infer token/profile fields.
 * Routes, login request and challenge_id are confirmed by Step 22.
 * Live /health and schema checks returned 503; sanitized successful responses are pending.
 */
export const LIVE_AUTH_CONTRACT=Object.freeze({
 confirmed:false,
 provenance:'Owner Step 22 confirms routes; successful token/profile response schema not supplied.',
 tokenPath:null,profilePath:null,idPath:null,loginPath:null,rolePath:null,
 sessionExpiryPath:null,sessionExpiryFormat:null,
 challengeExpiryPath:null,challengeExpiryFormat:null,
});
