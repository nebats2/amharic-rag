from aiohttp.abc import HTTPException
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from fastapi import HTTPException
from pydantic import SecretStr

from app.services.doc_processing import get_qdrant_vector_store
from app.settings.open_ai_config import get_openai_config_model
from app.settings.settings import Setting

app_setting = Setting()
openai_config_model = get_openai_config_model()


def get_openai_llm():
    if not openai_config_model.model or len(openai_config_model.model) <2:
        raise HTTPException(detail = "Openai chat model is not configerd", status_code=404)

    if not openai_config_model.api_key or len(openai_config_model.api_key) <2:
        raise HTTPException(detail = "Openai chat model api key is not configured", status_code=404)

    return   ChatOpenAI(
        model= openai_config_model.model,
        api_key=SecretStr(openai_config_model.api_key)
    )


def chat_document(user_question: str):
    qdrant_vector_store = get_qdrant_vector_store()
    retriever = qdrant_vector_store.as_retriever(search_kwargs={"k": 5})
    template = """
         You are a helpful assistant specialized in Ethiopian legal documents.
         Use the following retrieved documents to answer the question. 
         Always cite the sources (title and page number) in your final answer as a bullet list. 

         Context:
         {context}

         Question:
         {question}

         Answer (include citations as 'Title (page number)'):
         """

    prompt_template = ChatPromptTemplate.from_template(template)

    # RAG Chain
    rag_chain = (
            {
                "context": (lambda x: retriever.invoke(x["question"])),
                "question": RunnablePassthrough()
            }
            | prompt_template
            | get_openai_llm()
    )
    try:
        response = rag_chain.invoke({"question": user_question})
        return response.content
    except Exception as e:
        # Log and handle errors gracefully
        print(f"[chat_rag] Error: {e}")
        return "Sorry, I couldn't process your request at the moment."


def chat_rag(user_prompt: str):
    openai_llm = get_openai_llm()
    qdrant_vector_store = get_qdrant_vector_store()
    retriever = qdrant_vector_store.as_retriever(search_kwargs={"k": 5})
    context = retrieve_context(user_prompt, retriever)


    system_prompt = "You are a helpful assistant. Use the provided context to answer."
    full_prompt = f"Context:\n{context}\n\nUser: {user_prompt}\nAssistant:"

    response = openai_llm.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt},
        ]
    )

    return response.choices[0].message.content

def retrieve_context(query: str, retriever, k=5):
    results = retriever.get_relevant_documents(query)
    if not results:
        print(f"no similarity documents have found")
        return None
    else:
        print(f"Similarity document found : len = {len(results)}")
        context = "\n".join([doc.page_content for doc in results])
        return context
