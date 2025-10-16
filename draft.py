

def load_files(self, base_folder):
    """Create a dictionary from the folder structure."""
    files = {}
    base_path = Path(base_folder)
    
    print(f"Base folder: {base_path.absolute()}")
    print(f"Exists: {base_path.exists()}")
    
    # Let's see what's actually in the base folder
    print("\n=== Contents of base folder ===")
    if base_path.exists():
        for item in sorted(base_path.iterdir()):
            print(f"  {item.name} ({'dir' if item.is_dir() else 'file'})")
    
    # Try to find DO-* folders
    print("\n=== Looking for DO-* folders ===")
    do_folders = list(base_path.glob("DO-*"))
    print(f"Found {len(do_folders)} DO-* folders")
    for folder in do_folders:
        print(f"  - {folder.name}")
    
    # If we have DO-* folders, look inside them
    if do_folders:
        print("\n=== Contents of first DO-* folder ===")
        first_do = do_folders[0]
        for item in sorted(first_do.iterdir()):
            print(f"  {item.name} ({'dir' if item.is_dir() else 'file'})")
    
    # Try different glob patterns to see what matches
    print("\n=== Testing different patterns ===")
    patterns = [
        "**/*.pdf",  # All PDFs anywhere
        "DO-*/**/*.pdf",  # All PDFs under DO-* folders
        "DO-*/partners/*/client history/*.pdf",  # Your original pattern
        "DO-*/partners/*/*.pdf",  # Without "client history"
    ]
    
    for pattern in patterns:
        matches = list(base_path.glob(pattern))
        print(f"{pattern}: {len(matches)} files")
        if matches and len(matches) <= 5:
            for match in matches[:5]:
                print(f"    {match.relative_to(base_path)}")
    
    return files