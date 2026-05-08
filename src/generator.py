from fpdf import FPDF

class ForensicReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CONFIDENTIAL: DIGITAL FORENSIC REPORT', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(case_data, report_text, output_path="report.pdf"):
    pdf = ForensicReport()
    pdf.add_page()
    
    # --- Case Metadata ---
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Case ID: {case_data.get('id')}", 0, 1)
    pdf.cell(0, 10, f"Investigator: {case_data.get('name')}", 0, 1)
    pdf.cell(0, 10, f"Timestamp: {case_data.get('date')}", 0, 1)
    pdf.ln(10)

    # --- Analysis Content ---
    pdf.set_font('Arial', '', 11)
    # multi_cell handles long blocks of text and wraps them
    pdf.multi_cell(0, 10, report_text)
    
    pdf.output(output_path)
    return output_path