from fpdf import FPDF
import datetime
import os

class ReportGenerator:
    """
    Generates PDF and text reports for security audits.
    """
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_pdf_report(self, results, report_name=None):
        """
        Generates a PDF report summarizing the attack results.
        """
        if not report_name:
            report_name = f"security_audit_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        file_path = os.path.join(self.output_dir, report_name)
        
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Password Cracking & Credential Attack Suite", ln=True, align='C')
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Security Audit Report", ln=True, align='C')
        pdf.ln(10)
        
        # Date and Time
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.ln(5)
        
        # Results Section
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Audit Summary:", ln=True)
        pdf.set_font("Arial", '', 12)
        
        for key, value in results.items():
            if isinstance(value, dict):
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(200, 10, txt=f"{key.capitalize()}:", ln=True)
                pdf.set_font("Arial", '', 10)
                for k, v in value.items():
                    pdf.cell(200, 10, txt=f"  - {k}: {v}", ln=True)
            else:
                pdf.cell(200, 10, txt=f"{key.capitalize()}: {value}", ln=True)
        
        pdf.ln(10)
        
        # Conclusion
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Recommendations:", ln=True)
        pdf.set_font("Arial", '', 10)
        recommendations = [
            "Use passwords with at least 12 characters.",
            "Include a mix of uppercase, lowercase, numbers, and symbols.",
            "Avoid common words or personal information in passwords.",
            "Use a password manager to store complex passwords.",
            "Enable multi-factor authentication (MFA) where possible."
        ]
        for rec in recommendations:
            pdf.cell(200, 10, txt=f"  - {rec}", ln=True)
            
        pdf.output(file_path)
        print(f"PDF report generated: {file_path}")
        return file_path

    def generate_text_report(self, results, report_name=None):
        """
        Generates a plain text report summarizing the attack results.
        """
        if not report_name:
            report_name = f"security_audit_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
        file_path = os.path.join(self.output_dir, report_name)
        
        with open(file_path, 'w') as f:
            f.write("Password Cracking & Credential Attack Suite\n")
            f.write("Security Audit Report\n")
            f.write("="*40 + "\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("Audit Summary:\n")
            for key, value in results.items():
                if isinstance(value, dict):
                    f.write(f"{key.capitalize()}:\n")
                    for k, v in value.items():
                        f.write(f"  - {k}: {v}\n")
                else:
                    f.write(f"{key.capitalize()}: {value}\n")
            
            f.write("\nRecommendations:\n")
            recommendations = [
                "Use passwords with at least 12 characters.",
                "Include a mix of uppercase, lowercase, numbers, and symbols.",
                "Avoid common words or personal information in passwords.",
                "Use a password manager to store complex passwords.",
                "Enable multi-factor authentication (MFA) where possible."
            ]
            for rec in recommendations:
                f.write(f"  - {rec}\n")
                
        print(f"Text report generated: {file_path}")
        return file_path

if __name__ == "__main__":
    test_results = {
        "Target Hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
        "Hash Type": "SHA-256",
        "Status": "Password Found",
        "Password": "password",
        "Strength Analysis": {
            "Score": "0/4",
            "Entropy": "20.0 bits",
            "Crack Time": "instant"
        }
    }
    
    gen = ReportGenerator()
    gen.generate_pdf_report(test_results)
    gen.generate_text_report(test_results)
