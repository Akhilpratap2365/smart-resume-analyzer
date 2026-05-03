import PyPDF2


def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()
        return text
    except Exception:
        # Fallback: if the file is not a valid PDF (or PyPDF2 isn't able to parse),
        # try reading it as plain text. This helps during local testing when a
        # .pdf file may actually contain plain text.
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return ""
