from pathlib import Path


PROJECT_STRUCTURE = {
    "app": {
        "__init__.py": None,
        "main.py": None,

        "api": {
            "__init__.py": None,
            "routes.py": None,
        },

        "ocr": {
            "__init__.py": None,
            "preprocess.py": None,
            "pdf_processor.py": None,
            "tesseract_engine.py": None,
        },

        "extraction": {
            "__init__.py": None,
            "regex_extractor.py": None,
            "llm_extractor.py": None,
            "validator.py": None,
        },

        "models": {
            "__init__.py": None,
            "schemas.py": None,
        },

        "utils": {
            "__init__.py": None,
            "text_cleaner.py": None,
        },
    },

    "streamlit_app.py": None,

    "tests": {
        "test_ocr.py": None,
        "test_extraction.py": None,
        "test_validation.py": None,
    },

    "sample_documents": {},
    "output": {},

    "requirements.txt": None,
    ".env": None,
}


def create_structure(base_path: str = "RENTAl-AGREEMENT-PARSER"):
    """Create the rental agreement parser project structure."""

    root = Path(base_path)

    def create_items(current_path: Path, structure: dict):
        for name, content in structure.items():
            item_path = current_path / name

            if content is None:
                # Create file
                item_path.touch(exist_ok=True)
                print(f"Created file:   {item_path}")

            else:
                # Create directory
                item_path.mkdir(parents=True, exist_ok=True)
                print(f"Created folder: {item_path}")

                if isinstance(content, dict):
                    create_items(item_path, content)

    root.mkdir(parents=True, exist_ok=True)
    create_items(root, PROJECT_STRUCTURE)

    print("\nProject structure created successfully!")
    print(f"Location: {root.resolve()}")


if __name__ == "__main__":
    create_structure()

