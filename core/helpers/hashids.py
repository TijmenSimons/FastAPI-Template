"""
Module to encode and decode integers.
"""

from hashids import Hashids

from core.config import config
from core.exceptions.hashids import IncorrectHashIDException

hashids = Hashids(salt=config.HASH_ID_SALT, min_length=config.HASH_ID_MIN_LENGTH)


def encode(id_to_hash):
    """Hashids encode function"""
    return hashids.encode(id_to_hash)


def decode(hashed_ids):
    """Hashids decode function"""
    try:
        return hashids.decode(hashed_ids)

    except Exception as exc:
        raise IncorrectHashIDException from exc


def decode_single(hashed_ids) -> int:
    """Decode, return single ID"""
    real_ids = ()

    real_ids = decode(hashed_ids)

    if len(real_ids) < 1:
        raise IncorrectHashIDException

    return real_ids[0]


def check_id(hashed_id, func):
    """Check if the id returns a value from the provided function"""
    real_id = decode_single(hashed_id)
    obj = func(real_id)

    return obj


def try_decode(some_id):
    """Try and decode and id, which might be hashed"""

    try:
        some_id = int(some_id)
    except ValueError:
        some_id = decode_single(some_id)

    return some_id
