from pathlib import Path
import json
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from utils.logger import get_logger

logger=get_logger(__name__)

def load_pdfs(directory: str) -> list[Document]:
    documents=[]
    pdf_files=Path(directory).glob("*.pdf")

    for pdf in pdf_files:
        logger.info(f"Loading PDF: {pdf.name}")
        loader=PyPDFLoader(str(pdf))
        docs=loader.load()

        for doc in docs:
            doc.metadata["source"]=pdf.name
            doc.metadata["type"]="manual"
            documents.append(doc)
    return documents


def load_csv_logs(directory: str) -> list[Document]:
    documents = []
    csv_files = Path(directory).glob("*.csv")

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        content = df.to_csv(index=False) 

        documents.append(
            Document(
                page_content=content,
                metadata={"source": csv_file.name, "type": "maintenance_log"}
            )
        )

    return documents

def load_json_logs(directory: str):
    documents = []

    for json_file in Path(directory).glob("*.json"):
        with open(json_file, "r") as f:
            data = json.load(f)
        content = json.dumps(data)
        documents.append(
            Document(
                page_content=content,
                metadata={"source": json_file.name,"type":"maintenance_log"}
            )
        )

    return documents
def load_all_documents():
    documents=[]
    documents.extend(load_pdfs("data/manuals"))
    documents.extend(load_csv_logs("data/logs"))
    documents.extend(load_json_logs("data/logs"))

    logger.info(f"Total documents loaded: {len(documents)} " )
    return documents
