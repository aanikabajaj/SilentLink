from olm import Session
from olm import Account

def encrypt_message(sender_account, recipient_identity_key, recipient_one_time_key, message):
    session = Session.create_outbound(sender_account, recipient_identity_key, recipient_one_time_key)
    encrypted = session.encrypt(message)
    return encrypted, session.pickle("ERYx@03_15")

