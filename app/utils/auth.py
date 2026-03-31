import base64
from fastapi import HTTPException, Security, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from jose import JWTError, jwt
from sqlalchemy import text
from app.core.config import settings
from app.db.database import get_engine

bearer_scheme = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

ALLOWED_ROLES = {"ADMIN", "EMPLOYEE"}


def get_signing_key() -> bytes:
    """
    Spring Boot usa Decoders.BASE64.decode(secret).
    Python necesita padding correcto antes de decodificar.
    """
    secret = settings.JWT_SECRET
    # Agregar padding si la longitud no es múltiplo de 4
    missing_padding = len(secret) % 4
    if missing_padding:
        secret += "=" * (4 - missing_padding)
    return base64.b64decode(secret)


def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            get_signing_key(),
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido o expirado: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el token: {str(e)}",
        )


def get_role_from_db(email: str) -> str:
    query = "SELECT role FROM user WHERE email = :email AND deleted_at IS NULL LIMIT 1"
    try:
        with get_engine().connect() as conn:
            result = conn.execute(text(query), {"email": email})
            row = result.fetchone()
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Usuario '{email}' no encontrado",
                )
            return str(row[0]).upper()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error consultando rol: {str(e)}",
        )


def require_role(
    request:Request,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    api_key: str = Security(api_key_header),
):
    if request.method == "OPTIONS":
        return

    # API Key → acceso directo server-to-server
    if api_key and api_key == settings.API_KEY:
        return {"sub": "service_account", "role": "ADMIN"}

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere autenticación (Bearer token o X-API-Key)",
        )

    # 1. Decodificar JWT
    payload = decode_jwt(credentials.credentials)

    # 2. Extraer email del claim 'sub'
    email: str = payload.get("sub", "")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no contiene el claim 'sub'",
        )

    # 3. Buscar rol en la BD
    role = get_role_from_db(email)

    # 4. Validar rol
    if role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Rol '{role}' no tiene permisos. Se requiere ADMIN o EMPLOYEE.",
        )

    return {**payload, "role": role, "email": email}
