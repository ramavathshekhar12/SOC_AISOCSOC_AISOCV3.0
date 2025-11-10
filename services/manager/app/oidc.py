import os, httpx, time
from jose import jwt, jwk
from jose.utils import base64url_decode
from fastapi import HTTPException, Header

OIDC_ISSUER = os.getenv("OIDC_ISSUER", "")
OIDC_AUDIENCE = os.getenv("OIDC_AUDIENCE", "")
OIDC_JWKS_URL = os.getenv("OIDC_JWKS_URL", "")

_cached_jwks = None
_cached_at = 0

async def _get_jwks():
    global _cached_jwks, _cached_at
    if not _cached_jwks or (time.time() - _cached_at) > 3600:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(OIDC_JWKS_URL)
            r.raise_for_status()
            _cached_jwks = r.json()
            _cached_at = time.time()
    return _cached_jwks

async def require_roles(authorization: str | None = Header(None), roles: list[str] = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = authorization.split(" ", 1)[1]
    jwks = await _get_jwks()
    try:
        unverified = jwt.get_unverified_header(token)
        kid = unverified.get("kid")
        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if not key:
            raise Exception("kid not found")
        payload = jwt.decode(token, key, algorithms=[unverified["alg"]], audience=OIDC_AUDIENCE, issuer=OIDC_ISSUER)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"invalid token: {e}")
    user_roles = payload.get("roles") or payload.get("groups") or []
    if roles and not set(roles).intersection(set(user_roles)):
        raise HTTPException(status_code=403, detail="forbidden")
    return payload
