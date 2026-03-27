import argparse
import sys
import os

# Add current directory to path to allow importing modules from core and advanced
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from advanced.workflow_orchestrator import WorkflowOrchestrator
from core.hash_identifier import identify_hash
from core.dictionary_generator import generate_wordlist

def main():
    parser = argparse.ArgumentParser(description="Password Cracking & Credential Attack Suite")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 1. Identify Command
    identify_parser = subparsers.add_parser("identify", help="Identify a hash type")
    identify_parser.add_argument("hash", help="The hash string to identify")

    # 2. Generate Wordlist Command
    generate_parser = subparsers.add_parser("generate", help="Generate a custom wordlist")
    generate_parser.add_argument("--name", help="User's name")
    generate_parser.add_argument("--dob", help="User's date of birth (YYYY-MM-DD)")
    generate_parser.add_argument("--keywords", nargs="+", help="Keywords to include")
    generate_parser.add_argument("--output", default="wordlist.txt", help="Output file path")

    # 3. Audit Command (Main Attack Workflow)
    audit_parser = subparsers.add_parser("audit", help="Run a security audit / attack")
    audit_parser.add_argument("hash", help="The target hash string")
    audit_parser.add_argument("--type", choices=["dictionary", "brute_force"], default="dictionary", help="Type of attack")
    audit_parser.add_argument("--wordlist", help="Path to an existing wordlist file")
    audit_parser.add_argument("--mutate", action="store_true", help="Apply mutation rules for dictionary attack")
    audit_parser.add_argument("--max-len", type=int, default=4, help="Maximum password length for brute-force")
    audit_parser.add_argument("--charset", help="Custom charset for brute-force")
    audit_parser.add_argument("--name", help="User's name for wordlist generation")
    audit_parser.add_argument("--dob", help="User's date of birth for wordlist generation")
    audit_parser.add_argument("--keywords", nargs="+", help="Keywords for wordlist generation")

    args = parser.parse_args()

    if args.command == "identify":
        hash_type = identify_hash(args.hash)
        print(f"Identified Hash Type: {hash_type}")

    elif args.command == "generate":
        wordlist = generate_wordlist(name=args.name, dob=args.dob, keywords=args.keywords)
        with open(args.output, "w") as f:
            for word in wordlist:
                f.write(f"{word}\n")
        print(f"Wordlist generated and saved to: {args.output}")
        print(f"Total words: {len(wordlist)}")

    elif args.command == "audit":
        orchestrator = WorkflowOrchestrator()
        
        # Load wordlist if provided
        wordlist = []
        if args.wordlist:
            try:
                with open(args.wordlist, 'r') as f:
                    wordlist = [line.strip() for line in f]
            except FileNotFoundError:
                print(f"Error: Wordlist file not found at {args.wordlist}")
                return

        results = orchestrator.run_audit(
            args.hash,
            attack_type=args.type,
            wordlist=wordlist,
            use_mutations=args.mutate,
            max_length=args.max_len,
            charset=args.charset,
            name=args.name,
            dob=args.dob,
            keywords=args.keywords
        )

        if results:
            print("\n--- Audit Complete ---")
            if results['password']:
                print(f"Password Found: {results['password']}")
                print(f"Strength Score: {results['strength']['score']}/4")
            else:
                print("Password Not Found.")
            print(f"Reports generated in: {os.path.abspath('reports')}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
