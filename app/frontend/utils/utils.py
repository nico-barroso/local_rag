import base64
import os


def styles_file_opener(caller_file: str, file_name: str = "styles.css") -> str:
    """Read a CSS file located in the same directory as the caller file.

    Args:
        caller_file: Path of the calling file. Pass __file__ when the CSS
            is in the same directory as the caller.
        file_name: Name of the CSS file. Defaults to 'styles.css'.

    Returns:
        The contents of the CSS file as a string.
    """
    base_dir = os.path.dirname(caller_file)
    with open(os.path.join(base_dir, file_name)) as f:
        return f.read()


def font_to_base64(font_path: str) -> str:
    """Encode a font file to a base64 string for embedding in CSS.

    Args:
        font_path: Relative path to the font file from this module's directory.

    Returns:
        The font file encoded as a base64 string.
    """
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, font_path)
    with open(full_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
