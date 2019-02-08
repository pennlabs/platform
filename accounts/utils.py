from oauthlib.common import generate_client_id, UNICODE_ASCII_CHARACTER_SET
from django.contrib.auth.hashers import get_hasher
from accounts.serializers import StudentSerializer


def hash_client_secret(client_id, client_secret):
    return get_hasher(algorithm='default').encode(client_id, salt=client_secret)


def assign_client_secret(application):
    client_secret = generate_client_id(length=32, chars=UNICODE_ASCII_CHARACTER_SET)
    client_id = generate_client_id(length=32, chars=UNICODE_ASCII_CHARACTER_SET)
    hashed_secret = hash_client_secret(client_id, client_secret)
    setattr(application, 'client_id', client_id)
    setattr(application, 'hashed_secret', hashed_secret)
    return client_secret
