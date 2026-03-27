import itertools

def generate_wordlist(name=None, dob=None, keywords=None, common_passwords_file=None):
    """
    Generates a custom wordlist based on provided information and common patterns.
    """
    wordlist = set()

    # Add direct inputs
    if name:
        wordlist.add(name.lower())
        wordlist.add(name.capitalize())
        wordlist.add(name.upper())
    if dob:
        # Assuming DOB format YYYY-MM-DD or DD-MM-YYYY
        dob_parts = dob.replace('-', '').replace('/', '')
        wordlist.add(dob_parts)
        wordlist.add(dob_parts[0:4]) # Year
        wordlist.add(dob_parts[4:6]) # Month
        wordlist.add(dob_parts[6:8]) # Day
        wordlist.add(dob_parts[0:2] + dob_parts[2:4]) # DDMM
        wordlist.add(dob_parts[4:6] + dob_parts[6:8]) # MMYY
        wordlist.add(dob_parts[6:8] + dob_parts[0:4]) # DDYYYY

    if keywords:
        for kw in keywords:
            wordlist.add(kw.lower())
            wordlist.add(kw.capitalize())
            wordlist.add(kw.upper())

    # Add common patterns (e.g., append numbers, symbols)
    base_words = list(wordlist.copy())
    for word in base_words:
        for i in range(10):
            wordlist.add(f"{word}{i}")
            wordlist.add(f"{word}{i}{i}")
        wordlist.add(f"{word}!")
        wordlist.add(f"{word}@")
        wordlist.add(f"{word}#")
        wordlist.add(f"{word}123")
        wordlist.add(f"{word}2023")
        wordlist.add(f"{word}2024")

    # Add common passwords from a file
    if common_passwords_file:
        try:
            with open(common_passwords_file, 'r') as f:
                for line in f:
                    wordlist.add(line.strip())
        except FileNotFoundError:
            print(f"Warning: Common passwords file not found at {common_passwords_file}")

    return sorted(list(wordlist))

if __name__ == "__main__":
    print("Generating wordlist with name 'John' and DOB '1990-01-15':")
    wordlist1 = generate_wordlist(name="John", dob="1990-01-15")
    for word in wordlist1:
        print(word)
    print(f"Total words: {len(wordlist1)}\n")

    print("Generating wordlist with keywords 'company', 'project':")
    wordlist2 = generate_wordlist(keywords=["company", "project"])
    for word in wordlist2:
        print(word)
    print(f"Total words: {len(wordlist2)}\n")

    # Create a dummy common passwords file for testing
    with open("common_passwords.txt", "w") as f:
        f.write("password\n123456\nqwerty\n")

    print("Generating wordlist with name 'Alice' and common passwords file:")
    wordlist3 = generate_wordlist(name="Alice", common_passwords_file="common_passwords.txt")
    for word in wordlist3:
        print(word)
    print(f"Total words: {len(wordlist3)}\n")

    import os
    os.remove("common_passwords.txt") # Clean up dummy file
