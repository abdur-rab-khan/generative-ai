# Let's Install PyPDF to EXTRACT the text from the PDF
import os
import asyncio
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

load_dotenv()


async def extract_text_from_pdf(pdf_path):
    abs_path = os.path.abspath(pdf_path)
    loader = PyPDFLoader(abs_path)
    
    pages = []

    async for page in loader.alazy_load():
        pages.append(page)
    
    if pages:
        return pages
    else:
        print("No pages found in the PDF")

def store_on_vector_db(pages):
    # Vector Store is used to store the embeddings of the text from the PDF or any other source like ( websites etc)
    return InMemoryVectorStore.from_documents(pages,OpenAIEmbeddings())


if __name__ == "__main__":
    pdf_path = r"D:\Code\Python\lang-chain\tuto\data\layout-parser-paper.pdf"

    pages = asyncio.run(extract_text_from_pdf(pdf_path))

    vector_store = store_on_vector_db(pages)
    docs = vector_store.similarity_search("What is LayoutParser?", k=2)

    for doc in docs:
        print(f'Page {doc.metadata["page"]}: {doc.page_content[:300]}\n')

