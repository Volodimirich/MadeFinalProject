from fastapi_login import LoginManager


class NotAuthenticatedException(Exception):
    pass


SECRET = "6b079ed7f619921f438c93d454066a6b6ae62637b4473dc9"
manager = LoginManager(
    SECRET,
    token_url="/login",
    use_cookie=True,
    use_header=False,
    custom_exception=NotAuthenticatedException,
)


def hash_password(plaintext: str):
    return manager.pwd_context.hash(plaintext)


def verify_password(plaintext: str, hashed: str):
    return manager.pwd_context.verify(plaintext, hashed)
