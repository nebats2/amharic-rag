import re

from langchain_core.documents import Document

def split_text_by_lang(docs :list[Document])->  tuple[list[Document], list[Document]] | None:
    am_docs = []
    en_docs = []
    print("split docs by language started ...")
    for doc in docs:


        am, en = detect_text_chars(doc)
        if am:
            am_docs.extend(am)
        if en:
            en_docs.extend(en)

    return am_docs, en_docs

def detect_text_chars(doc: Document)-> tuple[list[Document], list[Document]]:
    text = doc.page_content
    # Extract Amharic (Ethiopic) text

    amharic_text = " ".join(re.findall(r"[\u1200-\u137F፡።፣፤\s]+", text)).strip()
    # Extract English (Latin letters, numbers, punctuation)

    english_text = " ".join(re.findall(r"[A-Za-z0-9.,!?;:'\"()\-–\s]+", text)).strip()

    eng_docs = []
    am_docs =  []
    if amharic_text:
        am_docs.append(Document(
            page_content=amharic_text,
            metadata={**doc.metadata, "language": "am"}
        ))
    if english_text:
        eng_docs.append(Document(
            page_content=english_text,
            metadata={**doc.metadata, "language": "en"}
        ))

    return am_docs, eng_docs

