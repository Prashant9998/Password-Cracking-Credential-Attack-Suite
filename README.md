# Password Cracking & Credential Attack Suite

An advanced, multi-functional tool for security auditing and educational purposes, focusing on credential security and attack simulation.

## Features

- **Hash Identification**: Automatically detect common hash types (MD5, SHA-1, SHA-256, etc.).
- **Dictionary Attack**: Perform attacks using wordlists with optional rule-based mutations.
- **Brute-Force Attack**: Configurable brute-force engine with customizable character sets and lengths.
- **Custom Wordlist Generation**: Create tailored wordlists based on user-provided information (name, DOB, keywords).
- **Password Strength Analysis**: Evaluate password security using entropy and the `zxcvbn` library.
- **Automated Reporting**: Generate comprehensive PDF and text reports summarizing audit results and recommendations.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/password_cracker.git
    cd password_cracker
    ```

3.  **Install dependencies**:
    ```bash
    pip install zxcvbn fpdf
    ```

## Usage

The suite is accessible via the `cli.py` command-line interface.

### 1. Identify a Hash
```bash
python cli.py identify 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

### 2. Generate a Custom Wordlist
```bash
python cli.py generate --name John --dob 1990-01-15 --keywords company project --output john_wordlist.txt
```

### 3. Run a Security Audit (Dictionary Attack)
```bash
python cli.py audit 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 --type dictionary --name John --mutate
```

### 4. Run a Security Audit (Brute-Force Attack)
```bash
python cli.py audit d41d8cd98f00b204e9800998ecf8427e --type brute_force --max-len 3
```

## Directory Structure

```
password_cracker/
├── cli.py                  # Main entry point
├── README.md               # Documentation
├── core/                   # Core cracking modules
│   ├── hash_identifier.py
│   ├── dictionary_generator.py
│   ├── brute_force_engine.py
│   ├── dictionary_attack_engine.py
│   └── rule_mutator.py
├── advanced/               # Advanced auditing modules
│   ├── password_strength_analyzer.py
│   ├── report_generator.py
│   └── workflow_orchestrator.py
├── data/                   # Data storage
│   ├── wordlists/
│   └── rules/
├── reports/                # Generated audit reports
└── ...
```

## Disclaimer

This tool is for **educational and authorized security testing purposes only**. Unauthorized access to computer systems is illegal. Use responsibly and ethically
final 

