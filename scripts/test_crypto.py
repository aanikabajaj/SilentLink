import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crypto.generate_keys import generate_user_keys
from crypto.rotate_keys import rotate_keys
from crypto.encrypt import encrypt_message
from crypto.decrypt import decrypt_message
from olm import Account
import json

# Step 1: Generate keys for user
generate_user_keys("alice@silentlink")

# Step 2: Create accounts
alice = Account()
alice.generate_one_time_keys(5)
bob = Account()
bob.generate_one_time_keys(5)

# Step 3: Encrypt a message from Alice to Bob
ciphertext, session_pickle = encrypt_message(
    alice,
    bob.identity_keys["curve25519"],
    list(bob.one_time_keys["curve25519"].values())[0],
    "Hello Bob!"
)

# Step 4: Decrypt the message
plaintext = decrypt_message(session_pickle, {
    "type": ciphertext["type"],
    "body": ciphertext["body"]
})
print("Decrypted:", plaintext)

