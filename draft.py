

from pathlib import Path

def load_files(self, base_folder):
    """Create a dictionary from the folder structure."""
    files = {}
    base_path = Path(base_folder)
    
    # Check if base path exists and print it
    print(f"Base folder: {base_path}")
    print(f"Base folder exists: {base_path.exists()}")
    print(f"Base folder is directory: {base_path.is_dir()}")
    
    # Find all PDFs in the structure with one glob pattern
    pattern = "DO-*/partners/*/client history/*.pdf"
    print(f"\nSearching for pattern: {pattern}")
    
    pdf_paths = list(base_path.glob(pattern))
    print(f"Found {len(pdf_paths)} PDF files")
    
    for i, pdf_path in enumerate(pdf_paths, 1):
        print(f"\n--- Processing file {i}/{len(pdf_paths)} ---")
        print(f"Full path: {pdf_path}")
        print(f"File exists: {pdf_path.exists()}")
        
        dd_folder = pdf_path.parents[3].name  # DO-* folder
        partner_folder = pdf_path.parents[1].name  # partner folder
        
        print(f"DD folder: {dd_folder}")
        print(f"Partner folder: {partner_folder}")
        
        # Extract text from PDF
        try:
            pdf_text = self.load(str(pdf_path))
            print(f"PDF text loaded, length: {len(pdf_text) if pdf_text else 0}")
        except Exception as e:
            print(f"Error loading PDF: {e}")
            continue
        
        # Build nested dictionary
        if dd_folder not in files:
            files[dd_folder] = {}
        files[dd_folder][partner_folder] = pdf_text
    
    print(f"\n=== Final result ===")
    print(f"Total DD folders: {len(files)}")
    for dd, partners in files.items():
        print(f"  {dd}: {len(partners)} partners")
    
    return files