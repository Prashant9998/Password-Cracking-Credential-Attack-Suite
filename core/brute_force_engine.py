import itertools
import hashlib
import string

def brute_force_attack(target_hash, hash_type, max_length=4, charset=string.ascii_lowercase + string.digits):
    """
    Simulates a brute-force attack against a target hash.
    """
    print(f"Starting brute-force attack for hash: {target_hash} (Type: {hash_type})")
    print(f"Max length: {max_length}, Charset: {charset}")

    for length in range(1, max_length + 1):
        for attempt in itertools.product(charset, repeat=length):
            candidate = ''.join(attempt)
            
            if hash_type == "MD5 / NTLM":
                hashed_candidate = hashlib.md5(candidate.encode()).hexdigest()
            elif hash_type == "SHA-1":
                hashed_candidate = hashlib.sha1(candidate.encode()).hexdigest()
            elif hash_type == "SHA-256":
                hashed_candidate = hashlib.sha256(candidate.encode()).hexdigest()
            elif hash_type == "SHA-384":
                hashed_candidate = hashlib.sha384(candidate.encode()).hexdigest()
            elif hash_type == "SHA-512":
                hashed_candidate = hashlib.sha512(candidate.encode()).hexdigest()
            else:
                print(f"Unsupported hash type: {hash_type}")
                return None

            if hashed_candidate == target_hash:
                print(f"Password found: {candidate}")
                return candidate

    print("Password not found within the specified parameters.")
    return None

if __name__ == "__main__":
    # Test MD5
    target_md5 = hashlib.md5(b"abc").hexdigest()
    result_md5 = brute_force_attack(target_md5, "MD5 / NTLM", max_length=3)
    print(f"Result MD5: {result_md5}\n")

    # Test SHA-1
    target_sha1 = hashlib.sha1(b"12").hexdigest()
    result_sha1 = brute_force_attack(target_sha1, "SHA-1", max_length=2, charset=string.digits)
    print(f"Result SHA-1: {result_sha1}\n")

    # Test SHA-256
    target_sha256 = hashlib.sha256(b"a1").hexdigest()
    result_sha256 = brute_force_attack(target_sha256, "SHA-256", max_length=2)
    print(f"Result SHA-256: {result_sha256}\n")

    # Test failure
    target_fail = hashlib.md5(b"abcd").hexdigest()
    result_fail = brute_force_attack(target_fail, "MD5 / NTLM", max_length=3)
    print(f"Result Fail: {result_fail}\n")
