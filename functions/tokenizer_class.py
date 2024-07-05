from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.globals import set_verbose, set_debug
from langchain_openai import AzureChatOpenAI
#from langchain_community.chat_models.openai import ChatOpenAI  
from langchain_community.embeddings.azure_openai import AzureOpenAIEmbeddings

from time import time
import os
import config

class EmbeddingProcessor:

    def __init__(self, model_path: str = config.EMBEDDING_MODEL, normalize_embedding: bool = True):

        self.reduce_template_string = """
        Você é um assistente de IA. A documentação está localizada em page_content.
        Você recebe as seguintes partes extraídas de um longo documento e uma pergunta. 
        Você só deve usar fontes e dados explicitamente listados como fontes no contexto. 
        Se a sua resposta for relevante, informe o texto em formato de manual, incluindo titulo do documento ou topico, datas de vigencia se possuir, referencias e nome do documento, do contrario apenas envie o texto de forma normal.
        

        NÃO use nenhum recurso externo, hiperlink ou referência para responder que não esteja listado.

        Se você não souber a resposta, basta dizer 'Não encontrei sua pergunta nos documentos internos. Por favor, forneça mais referências em sua pergunta.'. Não tente inventar uma resposta.
        Se a pergunta não for sobre algum documento, informe educadamente que você está preparado para responder apenas perguntas sobre a duvidas sobre documentos internos.
        Se o contexto não for relevante, não responda à pergunta usando seu próprio conhecimento sobre o assunto.

        {context}

        Pergunta: {question}
        """

        self.prompt = PromptTemplate(template=self.reduce_template_string, input_variables=["context","question"])
        #self.embedding_model = self.load_embedding_model(model_path, normalize_embedding)

        set_debug(config.DEBUG)
        set_verbose(config.DEBUG)

        self.llm_api = AzureChatOpenAI(
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_key=config.AZURE_OPENAI_API_KEY,
            api_version=config.AZURE_OPENAI_API_VERSION,
            deployment_name=config.AZURE_OPENAI_MODEL,
            model_name=config.AZURE_OPENAI_MODEL_NAME,
            max_tokens=1500,
            temperature=0.7,
            stop=[]
        )

        """
        self.llm_api = ChatOpenAI(
            model = config.OPENAI_LLM_MODEL,
            openai_api_key = config.OPENAI_API_KEY, 
            streaming = True, 
            max_tokens=900, 
            temperature=0.7
            )
        """
        self.embed_model = AzureOpenAIEmbeddings(
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_key=config.AZURE_OPENAI_API_KEY,
            azure_deployment="embeddings",
            model=config.EMBED_MODEL,
            chunk_size=500
        )

    def _document_to_dict(self, doc):
        clean_page_content = doc.page_content
        clean_title = doc.metadata.get('title')

        return {
            'page_content': clean_page_content,
            'metadata': {
                'title': clean_title,
                'page': doc.metadata.get('page'),
                'total_pages': doc.metadata.get('total_pages')
            }
        }

    def load_embedding_model(self, model_path, normalize_embedding=True):
        try:
            return HuggingFaceEmbeddings(
                model_name=model_path,
                model_kwargs={'device': config.DEVICE},
                encode_kwargs={'normalize_embeddings': normalize_embedding}
            )
        except Exception as e:
            print(f"Erro ao carregar o modelo de embeddings: {e}")
            return None


    def create_embeddings(self, chunks, storing_path):

        try:
            #vectorstore = FAISS.from_documents(chunks, self.embedding_model)
            vectorstore = FAISS.from_documents(chunks, self.embed_model)
            vectorstore.save_local(storing_path)
            return vectorstore
        
        except Exception as e:
            print(f"Erro ao criar embeddings: {e}")
            return None

    def load_embeddings(self, embedding_path):

        embedding_path = embedding_path.replace("\\", "/")
        index_path = f"{embedding_path}/index.faiss"

        if os.path.exists(index_path):
            #return FAISS.load_local(embedding_path, self.embedding_model, allow_dangerous_deserialization=True)
            return FAISS.load_local(embedding_path, self.embed_model, allow_dangerous_deserialization=True)

    def load_qa_chain(self, retriever, query):

        return RetrievalQA.from_chain_type(
            llm=self.llm_api,
            retriever=retriever,
            chain_type="stuff",
            return_source_documents=True,
            chain_type_kwargs={'prompt': query}
        )


    def create_chain(self, department: str):
        department = department.replace("/", "").replace("\\", "")
        vectorstore = self.load_embeddings(embedding_path=config.PATH_VECTOR_STORE + "/" + department)
        retriever = vectorstore.as_retriever(search_kwargs={"k":5})
        chain = self.load_qa_chain(retriever, self.prompt)

        return chain

    def get_response(self, query: str, chain):

        timestamp = str(int(time()))
        response = chain({'query': query})

        citations = [self._document_to_dict(doc) for doc in response['source_documents']]           

        response_data = {
            'tool': citations,
            'role':'assistant',
            'content': response.get('result')
        }

        return response_data
