from olm import Session

def decrypt_message(pickled_session, ciphertext):
    session = Session.from_pickle(pickled_session, "ERYx@03_15")
    plaintext = session.decrypt(ciphertext["type"], ciphertext["body"])
    return plaintext
