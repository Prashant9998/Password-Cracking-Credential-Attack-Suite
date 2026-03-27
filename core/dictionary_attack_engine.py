import hashlib

def dictionary_attack(target_hash, hash_type, wordlist, rule_mutator=None):
    """
    Performs a dictionary attack against a target hash.
    Optionally applies rule-based mutations to words in the wordlist.
    """
    print(f"Starting dictionary attack for hash: {target_hash} (Type: {hash_type})")

    for word in wordlist:
        candidates = [word]
        if rule_mutator:
            candidates.extend(rule_mutator.apply_rules(word))

        for candidate in candidates:
            hashed_candidate = None
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
                # This case should ideally be handled by hash_identifier first
                print(f"Unsupported hash type: {hash_type}")
                return None

            if hashed_candidate == target_hash:
                print(f"Password found: {candidate}")
                return candidate

    print("Password not found in the provided wordlist or with applied rules.")
    return None

if __name__ == "__main__":
    # Dummy RuleMutator for testing
    class DummyRuleMutator:
        def apply_rules(self, word):
            return [word + "123", word.capitalize(), word.upper()]

    dummy_mutator = DummyRuleMutator()

    # Test with a simple wordlist
    test_wordlist = ["password", "123456", "qwerty", "test"]

    # Test MD5
    target_md5 = hashlib.md5(b"password").hexdigest()
    print("\n--- Testing MD5 without mutator ---")
    result_md5 = dictionary_attack(target_md5, "MD5 / NTLM", test_wordlist)
    print(f"Result MD5: {result_md5}\n")

    target_md5_mutated = hashlib.md5(b"Password123").hexdigest()
    print("\n--- Testing MD5 with mutator ---")
    result_md5_mutated = dictionary_attack(target_md5_mutated, "MD5 / NTLM", ["password"], dummy_mutator)
    print(f"Result MD5 (mutated): {result_md5_mutated}\n")

    # Test SHA-1
    target_sha1 = hashlib.sha1(b"test").hexdigest()
    print("\n--- Testing SHA-1 without mutator ---")
    result_sha1 = dictionary_attack(target_sha1, "SHA-1", test_wordlist)
    print(f"Result SHA-1: {result_sha1}\n")

    # Test SHA-256 (failure case)
    target_sha256 = hashlib.sha256(b"nonexistent").hexdigest()
    print("\n--- Testing SHA-256 (failure) ---")
    result_sha256 = dictionary_attack(target_sha256, "SHA-256", test_wordlist)
    print(f"Result SHA-256: {result_sha256}\n")
