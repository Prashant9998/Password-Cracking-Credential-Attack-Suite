import zxcvbn
import math

def analyze_password_strength(password):
    """
    Analyzes the strength of a password using the zxcvbn library.
    Returns a dictionary with various metrics.
    """
    results = zxcvbn.zxcvbn(password)
    
    # Calculate basic entropy manually for additional context
    charset_size = 0
    if any(c.islower() for c in password): charset_size += 26
    if any(c.isupper() for c in password): charset_size += 26
    if any(c.isdigit() for c in password): charset_size += 10
    if any(not c.isalnum() for c in password): charset_size += 32 # Approximation for symbols

    entropy = 0
    if charset_size > 0:
        entropy = len(password) * math.log2(charset_size)

    analysis = {
        "password": password,
        "score": results['score'], # 0-4 (too guessable to very unguessable)
        "entropy": round(entropy, 2),
        "crack_times_display": results['crack_times_display'],
        "feedback": results['feedback'],
        "suggestions": results['feedback']['suggestions']
    }
    
    return analysis

if __name__ == "__main__":
    passwords = ["password", "123456", "John1990!", "CorrectHorseBatteryStaple", "aB1!c2@d3#"]
    
    for p in passwords:
        print(f"\nAnalyzing password: {p}")
        result = analyze_password_strength(p)
        print(f"Score: {result['score']}/4")
        print(f"Entropy: {result['entropy']} bits")
        print(f"Crack time (10k/sec): {result['crack_times_display']['offline_fast_hashing_1e10_per_second']}")
        print(f"Suggestions: {result['suggestions']}")
