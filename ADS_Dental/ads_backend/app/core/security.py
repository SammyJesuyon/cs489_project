from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.db.models import User, Role
from app.db.session import get_database
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    # Use timezone-aware datetime
    expire = datetime.now(datetime.UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_database)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fix SQLAlchemy where clause type issue
    # Ensure User.email is a Column and email is a str
    result = await db.execute(select(User).where(User.email == str(email)))
    user = result.scalar_one_or_none()
    if not user:
        raise credentials_exception
    return user

async def require_patient(current_user: User = Depends(get_current_user)):
    if hasattr(current_user, "role") and isinstance(current_user.role, str):
        if current_user.role.lower() != "patient":
            raise HTTPException(status_code=403, detail="Only patients can access this resource")
    elif hasattr(current_user, "roles"):  # if many-to-many relationship exists
        role_names = [r.name.lower() for r in current_user.roles]
        if "patient" not in role_names:
            raise HTTPException(status_code=403, detail="Only patients can access this resource")
    else:
        raise HTTPException(status_code=403, detail="Only patients can access this resource")
    return current_user