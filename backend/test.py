import hashlib

def hash_string(text):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(text.encode())
    return sha1_hash.hexdigest()

def main():
    text = "Hello Everyone"
    hashed_text = hash_string(text)
    print(f"Text: {text}")
    print(f"SHA1 Hash: {hashed_text}")

if __name__ == "__main__":
    main()