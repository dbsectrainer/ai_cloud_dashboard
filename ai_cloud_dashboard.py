# This file is maintained for backward compatibility
# Please use the modular version in src/app.py for new development

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

# Import and run the modular app
from app import main

if __name__ == "__main__":
    main()
