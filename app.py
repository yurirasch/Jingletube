"""
JingleTube - Entrypoint for Hugging Face Spaces
This file imports and launches the main Gradio app
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and launch the main app
from app import app

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
