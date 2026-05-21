import secrets
import string


def generate_random_code(length: int = 6) -> str:
    return "".join(secrets.choice(string.digits) for _ in range(length))


def generate_random_token(length: int = 32) -> str:
    return secrets.token_hex(length)


def generate_invitation_code(length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))
