"""
Generates the OpenAPI specification for the GreenAlpha API.
"""
import json
import sys
import os

# Add the GREENALPHA directory to the Python path to allow for correct module resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.main import app

def generate_openapi_spec():
    """Generates and saves the OpenAPI spec."""
    # Ensure the docs directory exists
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    openapi_spec = app.openapi()
    
    file_path = os.path.join(docs_dir, "openapi.json")
    with open(file_path, "w") as f:
        json.dump(openapi_spec, f, indent=2)
    
    print(f"✅ OpenAPI specification generated at {file_path}")

if __name__ == "__main__":
    generate_openapi_spec()
