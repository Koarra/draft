# folderA/setup_neuralkyc.py
import sys
from pathlib import Path

# Add the inner neuralkyc directory to Python path
project_root = Path(__file__).parent
neuralkyc_path = project_root / 'neuralkyc' / 'neuralkyc'

if neuralkyc_path.exists() and str(neuralkyc_path) not in sys.path:
    sys.path.insert(0, str(neuralkyc_path))






# folderA/main.py
import setup_neuralkyc  # MUST BE FIRST - before any other imports

# Now all your other imports
from processing.assessor import Assessor
# ... rest of your code

