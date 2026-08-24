import fitz


def extract_text_from_pdf(file_path):

    document = fitz.open(file_path)

    pages = []

    for page_number in range(len(document)):

        page = document[page_number]

        text = page.get_text()

        if text.strip():

            pages.append({
                "page": page_number + 1,
                "text": text
            })

    document.close()

    return pages