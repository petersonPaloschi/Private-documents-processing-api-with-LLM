from functions import documents_class, tokenizer_class
import config
import os

PATH_VECTOR_STORE = config.PATH_VECTOR_STORE
PATH_FILE = config.PATH_FILE

docs = documents_class.DocumentProcessor()
embed = tokenizer_class.EmbeddingProcessor()

dir_names = [dir_name for dir_name in os.listdir(PATH_FILE) if os.path.isdir(os.path.join(PATH_FILE, dir_name))]

for dir_name in dir_names:

    file_path = PATH_FILE + "/" + dir_name
    storing_path = PATH_VECTOR_STORE + "/" + dir_name

    docs_contents = docs.load_files(file_path)
    
    documents = docs.split_docs(docs_contents)
    vectorstore = embed.create_embeddings(documents, storing_path)


print("documentos treinados com sucesso")