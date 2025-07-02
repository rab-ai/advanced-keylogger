import argparse
import os
from modules.encryption import Encryptor

def main():
    parser = argparse.ArgumentParser(description="File Decryption Tool")
    parser.add_argument("key_file", help="Path to the encryption key file")
    parser.add_argument("encrypted_file", help="Path to the encrypted file")
    parser.add_argument("--output", help="Optional output file path")
    
    args = parser.parse_args()
    
    print(f"Initializing decryption with key: {args.key_file}")
    encryptor = Encryptor(key_file=args.key_file)
    
    # Handle custom output naming with "decrypt_" prefix if output not specified
    output = args.output
    if output is None:
        # Get the original filename
        filename = os.path.basename(args.encrypted_file)
        
        # Remove .enc extension if present
        if filename.endswith(".enc"):
            filename = filename[:-4]
            
        # Add "decrypt_" prefix
        filename = f"decrypt_{filename}"
        
        # Combine with original directory path
        output = os.path.join(os.path.dirname(args.encrypted_file), filename)
    
    print(f"Decrypting file: {args.encrypted_file}")
    print(f"Output will be saved to: {output}")
    encryptor.decrypt_file(args.encrypted_file, output_file=output)
    print("Decryption complete!")

if __name__ == "__main__":
    main()