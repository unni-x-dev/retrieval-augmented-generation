swagger_description = """
    This project implements a **basic Retrieval-Augmented Generation (RAG)
    pipeline**
    using **FastAPI** and **MongoDB** as the data store.

    ### 📌 What is RAG?
    Retrieval-Augmented Generation (RAG) combines:
    - 🔎 **Retrieval** → Fetching relevant documents from MongoDB
    - ✍️ **Generation** → Using a language model to generate grounded
                         context-aware answers

    This approach helps:
    - ✅ Reduce hallucinations from the model
    - ✅ Provide up-to-date answers from your own knowledge base
    - ✅ Make APIs more reliable and adaptable

    ### 🚀 Features in this API
    - **Health Check Endpoint** → Verify that the service is running
    - **Standard Response Schemas** →
    - `BaseResponse`
    - `BaseHttpResponse`
    - `BaseHttpPaginatedResponse`
    - **Extensible Design** →
            Ready to plug in document retrieval + generation logic

    ---
    📖 Use this as a starting point for building production-ready
"""
