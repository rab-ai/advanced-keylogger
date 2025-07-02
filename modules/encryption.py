from cryptography.fernet import Fernet
import os
import base64

class Encryptor:
    def __init__(self, key_file="encryption.key"):
        """Initialize the encryptor."""
        self.key_file = key_file
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)
    
    def _load_or_generate_key(self):
        """Load existing key or generate a new one."""
        if os.path.exists(self.key_file):
            # Load existing key
            with open(self.key_file, "rb") as key_file:
                key = key_file.read()
        else:
            # Generate a new key
            key = Fernet.generate_key()
            # Save the key
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
            print(f"New encryption key generated and saved to {self.key_file}")
        
        return key
    
    def encrypt_file(self, input_file, output_file=None):
        """Encrypt a file."""
        if output_file is None:
            output_file = input_file + ".enc"
        
        try:
            # Read the file content
            with open(input_file, "rb") as f:
                data = f.read()
            
            # Encrypt the data
            encrypted_data = self.cipher.encrypt(data)
            
            # Write encrypted data to output file
            with open(output_file, "wb") as f:
                f.write(encrypted_data)
            
            print(f"File encrypted: {input_file} -> {output_file}")
            return output_file
        except Exception as e:
            print(f"Encryption error: {e}")
            return None
    
    def decrypt_file(self, input_file, output_file=None):
        """Decrypt a file."""
        if output_file is None:
            # Remove .enc extension if it exists
            if input_file.endswith(".enc"):
                output_file = input_file[:-4]
            else:
                output_file = input_file + ".dec"
        
        try:
            # Read the encrypted data
            with open(input_file, "rb") as f:
                encrypted_data = f.read()
            
            # Decrypt the data
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Write decrypted data to output file
            with open(output_file, "wb") as f:
                f.write(decrypted_data)
            
            print(f"File decrypted: {input_file} -> {output_file}")
            return output_file
        except Exception as e:
            print(f"Decryption error: {e}")
            return None