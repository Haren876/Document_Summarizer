import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def create_chunks(pages, chunk_size=12000):

    chunks = []

    current_text = ""

    current_pages = []


    for page in pages:

        page_text = page["text"]


        if (
            len(current_text) + len(page_text)
            > chunk_size
            and current_text
        ):

            chunks.append({
                "text": current_text,
                "pages": current_pages
            })

            current_text = ""

            current_pages = []


        current_text += "\n\n" + page_text

        current_pages.append(
            page["page"]
        )


    if current_text.strip():

        chunks.append({
            "text": current_text,
            "pages": current_pages
        })


    return chunks


def summarize_chunk(chunk):

    prompt = f"""
You are an expert document analysis assistant.

Analyze this document section carefully.

Create a detailed summary containing:

1. Main topic
2. Important concepts
3. Important definitions
4. Detailed explanations
5. Examples
6. Important formulas
7. Algorithms or methods
8. Advantages
9. Disadvantages
10. Important facts
11. Key conclusions

Rules:

- Only use information present in the document.
- Do not invent information.
- Preserve technical terms.
- Explain difficult concepts clearly.
- Preserve formulas whenever possible.

Document pages:

{chunk["pages"]}

Document content:

{chunk["text"]}
"""


    response = client.responses.create(

        model="YOUR_AVAILABLE_MODEL",

        input=prompt

    )


    return response.output_text


def create_final_summary(summaries):

    combined = ""


    for i, summary in enumerate(summaries):

        combined += (
            f"\n\n===== SECTION {i + 1} =====\n"
        )

        combined += summary


    prompt = f"""
You are an expert academic document summarizer.

The following are summaries from different
sections of the same document.

Create ONE comprehensive final summary.

Use this structure:

# DOCUMENT OVERVIEW

# DETAILED SUMMARY

# IMPORTANT CONCEPTS

# IMPORTANT DEFINITIONS

# FORMULAS

# ALGORITHMS AND METHODS

# IMPORTANT EXAMPLES

# KEY TAKEAWAYS

# CONCLUSION

Rules:

- Do not invent information.
- Preserve important technical information.
- Remove unnecessary repetition.
- Make the explanation easy to understand.
- Preserve important formulas.

Section summaries:

{combined}
"""


    response = client.responses.create(

        model="YOUR_AVAILABLE_MODEL",

        input=prompt

    )


    return response.output_text