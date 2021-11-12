# GENERATE ENCRYPTED PASSWORD WITH BCRYPT
# STORE THE DECODED HASHED PASSWORD IN YOUR MONGO DB IN THE USER COLLECTION ROOT
# ALONG WITH A USERNAME
# PASSWORD HAS TO BE ENCODED INTO BYTES
import bcrypt


def encrypt_password(password):

    # THIS HASHES THE PASSWORD ABOVE
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    return hashed.decode("utf-8").strip()