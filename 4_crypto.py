import os
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# ==========================================
# PHASE 1: PASSWORD HASHING (BCRYPT) - ONE-WAY
# ==========================================
def run_one_way_hashing_demo():
    print("\n" + "="*50)
    print("PHASE 1: ONE-WAY CRYPTOGRAPHIC HASHING (BCRYPT)")
    print("="*50)
    
    raw_user_password = "SuperSecureUserPassword123"
    print(f"[INPUT] Plaintext Password: {raw_user_password}")
    
    # Generate a secure mathematical Salt and hash the password in one atomic step
    # bcrypt automatically manages the salt generation and embeds it directly into the output string
    # rounds=12 sets the computational work factor (slowness feature) to resist brute-force
    password_bytes = raw_user_password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
    
    print(f"[STORED IN DATABASE] Hash Value: {hashed_password.decode('utf-8')}")
    
    # Simulating a user login attempt
    print("\n--- Simulating Authentication Verification Checks ---")
    correct_attempt = "SuperSecureUserPassword123"
    wrong_attempt = "SuperSecureUserPassword1234"
    
    # Verification Rule: You never decrypt a hash. You hash the incoming attempt and compare vectors.
    is_correct_match = bcrypt.checkpw(correct_attempt.encode('utf-8'), hashed_password)
    is_wrong_match = bcrypt.checkpw(wrong_attempt.encode('utf-8'), hashed_password)
    
    print(f"Attempt: '{correct_attempt}' -> Authenticated? {is_correct_match}")
    print(f"Attempt: '{wrong_attempt}' -> Authenticated? {is_wrong_match}")


# ==========================================
# PHASE 2: SYMMETRIC ENCRYPTION (FERNET) - TWO-WAY
# ==========================================
def run_symmetric_encryption_demo():
    print("\n" + "="*50)
    print("PHASE 2: TWO-WAY SYMMETRIC ENCRYPTION (SHARED KEY)")
    print("="*50)
    
    confidential_payload = "CRITICAL_METRIC: Company Quarterly Revenue is $4.2M"
    print(f"[INPUT] Secret Plaintext Data: {confidential_payload}")
    
    # Generate a single private key that will handle both locking and unlocking
    shared_secret_key = Fernet.generate_key()
    print(f"[SHARED SECRET KEY] Base64 Token: {shared_secret_key.decode('utf-8')}")
    
    # Initialize the symmetric cryptographic engine
    cipher_suite = Fernet(shared_secret_key)
    
    # 1. Encrypting the payload (Two-Way Locking)
    encrypted_bytes = cipher_suite.encrypt(confidential_payload.encode('utf-8'))
    print(f"[TRANSMITTING OVER NETWORK] Ciphertext: {encrypted_bytes.decode('utf-8')}")
    
    # 2. Decrypting the payload (Two-Way Unlocking)
    decrypted_bytes = cipher_suite.decrypt(encrypted_bytes)
    print(f"[DECRYPTED AT DESTINATION] Recovered Data: {decrypted_bytes.decode('utf-8')}")


# ==========================================
# PHASE 3: ASYMMETRIC ENCRYPTION (RSA) - KEY PAIRS
# ==========================================
def run_asymmetric_encryption_demo():
    print("\n" + "="*50)
    print("PHASE 3: TWO-WAY ASYMMETRIC ENCRYPTION (PUBLIC/PRIVATE KEY PAIR)")
    print("="*50)
    
    sensitive_token = "CLOUD_DATABASE_ROOT_PASSWORD_2026"
    print(f"[INPUT] Plaintext Token to Transfer: {sensitive_token}")
    
    # 1. Generate mathematically linked key pair at destination
    # public_exponent=65537 is a standard cryptographic prime choice
    # key_size=2048 defines standard production bit-strength
    private_key_instance = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key_instance = private_key_instance.public_key()
    print("LOG: Mathematical Private Key and Public Key pair successfully compiled.")
    
    # 2. Encrypt using the PUBLIC KEY (Anyone can do this)
    # OAEP padding ensures identical plaintexts result in completely different ciphertexts every time
    encrypted_token = public_key_instance.encrypt(
        sensitive_token.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"[ENCRYPTED WITH PUBLIC KEY] Hex Ciphertext Output:\n{encrypted_token.hex()[:120]}...")
    
    # 3. Decrypt exclusively using the matching PRIVATE KEY (Only the receiver can do this)
    decrypted_token = private_key_instance.decrypt(
        encrypted_token,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"[DECRYPTED WITH PRIVATE KEY] Successfully Restored: {decrypted_token.decode('utf-8')}")


# ==========================================
# MAIN EXECUTION INTERFACE
# ==========================================
if __name__ == "__main__":
    print("=== STARTING ENTERPRISE CRYPTOGRAPHIC PIPELINE LAB ===")
    
    run_one_way_hashing_demo()
    run_symmetric_encryption_demo()
    run_asymmetric_encryption_demo()
    
    print("\n" + "="*50)
    print("Cryptographic Sandbox Environment Successfully Completed.")