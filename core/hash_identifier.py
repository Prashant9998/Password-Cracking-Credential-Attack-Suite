import hashlib

def identify_hash(hash_string):
    """
    Identifies the type of hash based on its length and common patterns.
    """
    hash_length = len(hash_string)

    if not hash_string.isalnum():
        return "Unknown (contains non-alphanumeric characters)"

    if hash_length == 32:
        # MD5, NTLM (often 32 hex chars)
        return "MD5 / NTLM"
    elif hash_length == 40:
        # SHA-1
        return "SHA-1"
    elif hash_length == 64:
        # SHA-256
        return "SHA-256"
    elif hash_length == 96:
        # SHA-384
        return "SHA-384"
    elif hash_length == 128:
        # SHA-512
        return "SHA-512"
    else:
        return "Unknown"

if __name__ == "__main__":
    test_hashes = {
        "d41d8cd98f00b204e9800998ecf8427e": "MD5 / NTLM",  # empty string MD5
        "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3": "SHA-1", # 'test' SHA-1
        "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08": "SHA-256", # 'test' SHA-256
        "7c4a8d09ca3762af61e59520943dc26494f8941b": "SHA-1", # 'password' SHA-1
        "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92": "SHA-256", # 'password' SHA-256
        "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8": "SHA-256", # 'hello' SHA-256
        "notahash": "Unknown",
        "12345678901234567890123456789012": "MD5 / NTLM",
        "1234567890123456789012345678901234567890": "SHA-1",
        "1234567890123456789012345678901234567890123456789012345678901234": "SHA-256",
    }

    for h, expected in test_hashes.items():
        result = identify_hash(h)
        print(f"Hash: {h}\nIdentified: {result}\nExpected: {expected}\n{'PASS' if result == expected else 'FAIL'}\n")

    # Example of a hash that might be tricky due to non-alphanumeric characters
    print(f"Hash: {'$1$salt$hashvalue'}\nIdentified: {identify_hash('$1$salt$hashvalue')}\n")
