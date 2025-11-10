import { UserManager, WebStorageStateStore } from 'oidc-client-ts'
const authority = import.meta.env.VITE_OIDC_AUTHORITY
const client_id = import.meta.env.VITE_OIDC_CLIENT_ID
const redirect_uri = import.meta.env.VITE_OIDC_REDIRECT_URI || window.location.origin + '/'
const scope = 'openid profile email offline_access'
export const mgr = new UserManager({
  authority, client_id, redirect_uri, response_type: 'code', scope,
  userStore: new WebStorageStateStore({ store: window.localStorage })
})
export async function login() { await mgr.signinRedirect() }
export async function logout() { await mgr.signoutRedirect() }
export async function handleRedirect() { try { return await mgr.signinCallback(); } catch(e) { console.error(e) } }
export async function getUser() { return await mgr.getUser() }
export function bearer(token){ return { headers: { Authorization: `Bearer ${token}` } } }
