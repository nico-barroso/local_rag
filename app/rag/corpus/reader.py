from pathlib import Path

import fitz  # type: ignore

root_url = "./docs"


def get_path(path_url: str) -> list[str]:
    path = Path(path_url)

    # Validations
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path_url}")
    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path_url}")

    return [str(p) for p in path.glob("*.pdf")]


def read_pdf(urls: list[str]) -> list[dict]:
    try:
        pages = []
        for path in urls:
            doc = fitz.open(path)
            for page in doc:
                pages.append(
                    {
                        "doc_path": path,
                        "page": page.number + 1,
                        "text": page.get_text(),
                    }
                )
            doc.close()
        return pages
    except Exception as e:
        print("There was an error", e)
        return [{}]


print(get_path(root_url))
print(read_pdf(get_path(root_url)))
