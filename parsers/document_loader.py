"""
parsers/document_loader.py
Extracts plain text from an uploaded file (pdf, docx, txt, csv) so it can be
fed into the LLM as context.
"""

import csv
import io


def extract_text(uploaded_file, max_chars: int = 20000) -> str:
    """Takes a Streamlit UploadedFile and returns extracted plain text.
    Falls back gracefully with an error message string if parsing fails,
    so the caller never has to worry about exceptions."""
    if uploaded_file is None:
        return ""

    name = uploaded_file.name.lower()
    uploaded_file.seek(0)

    try:
        if name.endswith(".pdf"):
            return _extract_pdf(uploaded_file, max_chars)
        if name.endswith(".docx"):
            return _extract_docx(uploaded_file, max_chars)
        if name.endswith(".csv"):
            return _extract_csv(uploaded_file, max_chars)
        # default: treat as plain text
        return _extract_txt(uploaded_file, max_chars)
    except Exception as exc:  # noqa: BLE001
        return f"[Could not parse '{uploaded_file.name}': {exc}]"


def _extract_pdf(f, max_chars: int) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("pypdf is not installed (pip install pypdf)") from exc

    reader = PdfReader(f)
    chunks = []
    for page in reader.pages:
        chunks.append(page.extract_text() or "")
        if sum(len(c) for c in chunks) > max_chars:
            break
    return "\n".join(chunks)[:max_chars]


def _extract_docx(f, max_chars: int) -> str:
    try:
        import docx
    except ImportError as exc:
        raise RuntimeError("python-docx is not installed (pip install python-docx)") from exc

    document = docx.Document(f)
    text = "\n".join(p.text for p in document.paragraphs)
    return text[:max_chars]


def _extract_csv(f, max_chars: int) -> str:
    raw = f.read().decode("utf-8", errors="ignore")
    reader = csv.reader(io.StringIO(raw))
    rows = list(reader)
    preview = rows[:200]  # cap rows to keep prompt sane
    formatted = "\n".join(", ".join(row) for row in preview)
    return formatted[:max_chars]


def _extract_txt(f, max_chars: int) -> str:
    raw = f.read()
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", errors="ignore")
    return raw[:max_chars]
