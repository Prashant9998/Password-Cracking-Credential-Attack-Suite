from core.hash_identifier import identify_hash
from core.dictionary_generator import generate_wordlist
from core.brute_force_engine import brute_force_attack
from core.dictionary_attack_engine import dictionary_attack
from core.rule_mutator import RuleMutator
from advanced.password_strength_analyzer import analyze_password_strength
from advanced.report_generator import ReportGenerator

class WorkflowOrchestrator:
    """
    Manages the overall workflow of the password cracking and security audit process.
    """
    def __init__(self):
        self.rule_mutator = RuleMutator()
        self.report_generator = ReportGenerator()

    def run_audit(self, target_hash, attack_type="dictionary", **kwargs):
        """
        Runs a complete security audit based on the provided target hash and parameters.
        """
        print(f"\n--- Starting Security Audit ---")
        print(f"Target Hash: {target_hash}")
        print(f"Attack Type: {attack_type}")

        # 1. Hash Identification
        hash_type = identify_hash(target_hash)
        print(f"Identified Hash Type: {hash_type}")

        if hash_type == "Unknown":
            print("Error: Could not identify hash type. Please specify manually.")
            return None

        result = None
        # 2. Attack Execution
        if attack_type == "dictionary":
            wordlist = kwargs.get('wordlist', [])
            if not wordlist:
                # If no wordlist provided, generate one from user info if available
                wordlist = generate_wordlist(
                    name=kwargs.get('name'),
                    dob=kwargs.get('dob'),
                    keywords=kwargs.get('keywords')
                )
            
            use_mutations = kwargs.get('use_mutations', False)
            mutator = self.rule_mutator if use_mutations else None
            result = dictionary_attack(target_hash, hash_type, wordlist, mutator)

        elif attack_type == "brute_force":
            max_length = kwargs.get('max_length', 4)
            charset = kwargs.get('charset', None)
            if charset:
                result = brute_force_attack(target_hash, hash_type, max_length, charset)
            else:
                result = brute_force_attack(target_hash, hash_type, max_length)

        # 3. Strength Analysis (if password found)
        strength_info = None
        if result:
            print(f"Password Found: {result}")
            strength_info = analyze_password_strength(result)
        else:
            print("Password Not Found.")

        # 4. Report Generation
        audit_results = {
            "target_hash": target_hash,
            "hash_type": hash_type,
            "attack_type": attack_type,
            "status": "Success" if result else "Failed",
            "password_found": result if result else "N/A"
        }
        
        if strength_info:
            audit_results["strength_analysis"] = {
                "score": f"{strength_info['score']}/4",
                "entropy": f"{strength_info['entropy']} bits",
                "crack_time": strength_info['crack_times_display']['offline_fast_hashing_1e10_per_second']
            }

        pdf_report = self.report_generator.generate_pdf_report(audit_results)
        text_report = self.report_generator.generate_text_report(audit_results)

        return {
            "password": result,
            "strength": strength_info,
            "reports": [pdf_report, text_report]
        }

if __name__ == "__main__":
    # Test dictionary attack with mutations
    import hashlib
    orchestrator = WorkflowOrchestrator()
    
    # Test Case 1: Dictionary Attack
    target_1 = hashlib.md5(b"Password123").hexdigest()
    print("\n--- Test Case 1: Dictionary Attack ---")
    orchestrator.run_audit(target_1, attack_type="dictionary", name="John", use_mutations=True)

    # Test Case 2: Brute Force Attack
    target_2 = hashlib.sha1(b"abc").hexdigest()
    print("\n--- Test Case 2: Brute Force Attack ---")
    orchestrator.run_audit(target_2, attack_type="brute_force", max_length=3)
