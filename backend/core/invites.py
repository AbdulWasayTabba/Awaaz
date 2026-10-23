import hashlib
import secrets

# no 0/O/1/I so codes are easy to read aloud
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def generate_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(8))


def hash_code(code: str) -> bytes:
    # same idea as password hashing, but a fast hash is fine for a random code
    return hashlib.sha256(code.strip().upper().encode()).digest()