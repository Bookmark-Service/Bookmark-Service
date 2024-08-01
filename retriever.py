def retriever(vectorstore) :
    rt = vectorstore.as_retriever()
    return rt
