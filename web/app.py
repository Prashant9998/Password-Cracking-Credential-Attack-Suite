from flask import Flask, render_template, request, jsonify, send_file
import sys
import os
import json
from datetime import datetime

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.hash_identifier import identify_hash
from core.dictionary_generator import generate_wordlist
from core.brute_force_engine import brute_force_attack
from core.dictionary_attack_engine import dictionary_attack
from core.rule_mutator import RuleMutator
from advanced.password_strength_analyzer import analyze_password_strength
from advanced.report_generator import ReportGenerator

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Define reports directory based on environment (Vercel has read-only filesystem except for /tmp)
if os.environ.get('VERCEL'):
    reports_dir = os.path.join('/tmp', 'reports')
else:
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports')

# Initialize components
rule_mutator = RuleMutator()
report_generator = ReportGenerator(output_dir=reports_dir)

@app.route('/')
def index():
    """Render the main dashboard."""
    return render_template('index.html')

@app.route('/api/identify', methods=['POST'])
def api_identify():
    """API endpoint to identify hash type."""
    try:
        data = request.json
        hash_string = data.get('hash', '').strip()
        
        if not hash_string:
            return jsonify({'error': 'Hash string is required'}), 400
        
        hash_type = identify_hash(hash_string)
        return jsonify({
            'hash': hash_string,
            'type': hash_type,
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/generate-wordlist', methods=['POST'])
def api_generate_wordlist():
    """API endpoint to generate custom wordlist."""
    try:
        data = request.json
        name = data.get('name', '').strip()
        dob = data.get('dob', '').strip()
        keywords = data.get('keywords', [])
        
        wordlist = generate_wordlist(name=name if name else None, dob=dob if dob else None, keywords=keywords if keywords else None)
        
        return jsonify({
            'wordlist': wordlist,
            'count': len(wordlist),
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/attack', methods=['POST'])
def api_attack():
    """API endpoint to run an attack (dictionary or brute-force)."""
    try:
        data = request.json
        target_hash = data.get('hash', '').strip()
        attack_type = data.get('type', 'dictionary')
        
        if not target_hash:
            return jsonify({'error': 'Target hash is required'}), 400
        
        # Identify hash type
        hash_type = identify_hash(target_hash)
        if hash_type == "Unknown":
            return jsonify({'error': 'Could not identify hash type'}), 400
        
        result = None
        
        if attack_type == 'dictionary':
            wordlist = data.get('wordlist', [])
            if not wordlist:
                # Generate wordlist from provided data
                wordlist = generate_wordlist(
                    name=data.get('name'),
                    dob=data.get('dob'),
                    keywords=data.get('keywords')
                )
            
            use_mutations = data.get('use_mutations', False)
            mutator = rule_mutator if use_mutations else None
            result = dictionary_attack(target_hash, hash_type, wordlist, mutator)
        
        elif attack_type == 'brute_force':
            max_length = data.get('max_length', 4)
            charset = data.get('charset', None)
            result = brute_force_attack(target_hash, hash_type, max_length, charset)
        
        # Analyze password strength if found
        strength_info = None
        if result:
            strength_info = analyze_password_strength(result)
        
        # Generate reports
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
        
        report_generator.generate_pdf_report(audit_results)
        report_generator.generate_text_report(audit_results)
        
        return jsonify({
            'password': result,
            'strength': strength_info,
            'hash_type': hash_type,
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/reports', methods=['GET'])
def api_reports():
    """API endpoint to list generated reports."""
    try:
        if not os.path.exists(reports_dir):
            return jsonify({'reports': [], 'success': True})
        
        files = os.listdir(reports_dir)
        reports = [f for f in files if f.endswith('.pdf') or f.endswith('.txt')]
        reports.sort(reverse=True)
        
        return jsonify({
            'reports': reports[:10],  # Return last 10 reports
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/download-report/<filename>', methods=['GET'])
def api_download_report(filename):
    """API endpoint to download a report."""
    try:
        file_path = os.path.join(reports_dir, filename)
        
        # Security check: ensure file is in reports directory
        if not os.path.abspath(file_path).startswith(os.path.abspath(reports_dir)):
            return jsonify({'error': 'Invalid file path'}), 403
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
