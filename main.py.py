import os
import tempfile

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from document_parser import extract_text_from_pdf

from summarizer import (
    create_chunks,
    summarize_chunk,
    create_final_summary
)


load_dotenv()


app = FastAPI(
    title="Document AI Summarizer"
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


@app.get("/")
def home():

    return {
        "message":
        "Document AI backend is running"
    }


@app.post("/summarize")
async def summarize_document(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        return {
            "success": False,
            "error":
            "Only PDF files are supported."
        }


    file_data = await file.read()


    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )


    try:

        temp_file.write(file_data)

        temp_file.close()


        # 1. Extract PDF text

        pages = extract_text_from_pdf(
            temp_file.name
        )


        if not pages:

            return {
                "success": False,
                "error":
                "Could not extract PDF text."
            }


        # 2. Split document

        chunks = create_chunks(
            pages
        )


        # 3. Summarize each chunk

        summaries = []


        for chunk in chunks:

            summary = summarize_chunk(
                chunk
            )

            summaries.append(summary)


        # 4. Create final summary

        final_summary = create_final_summary(
            summaries
        )


        return {

            "success": True,

            "filename":
            file.filename,

            "pages":
            len(pages),

            "chunks":
            len(chunks),

            "summary":
            final_summary

        }


    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }


    finally:

        if os.path.exists(
            temp_file.name
        ):

            os.remove(
                temp_file.name
            )