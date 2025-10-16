from pathlib import Path

def load_files(self, base_folder):
    """Create a dictionary from the folder structure."""
    files = {}
    base_path = Path(base_folder)
    
    # Find all PDFs in the structure with one glob pattern
    for pdf_path in base_path.glob("DO-*/partners/*/client history/*.pdf"):
        dd_folder = pdf_path.parents[3].name  # DO-* folder
        partner_folder = pdf_path.parents[1].name  # partner folder
        
        # Extract text from PDF
        pdf_text = self.load(str(pdf_path))
        
        # Build nested dictionary
        if dd_folder not in files:
            files[dd_folder] = {}
        files[dd_folder][partner_folder] = pdf_text
    
    return files