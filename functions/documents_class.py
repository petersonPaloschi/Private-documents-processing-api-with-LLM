from typing import List
from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.text import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyMuPDFLoader

import tiktoken

import os
import re

class DocumentProcessor:
    """
    Classe para processar documentos de vários formatos, incluindo carregamento e divisão em chunks.
    """

    def normalize_text(self, s: str):

        s = re.sub(r'\s+',  ' ', s).strip()
        s = re.sub(r". ,","",s)
        s = s.replace("..",".")
        s = s.replace(". .",".")
        s = s.replace("\n", "")

        s = re.sub(r'\.{2,}', '.', s)
        s = re.sub(r'\r+', ' ', s)
        s = re.sub(r'\t+', ' ', s)

        return s.strip().lower()


    def load_files(sel, file_path: str) -> List[str]:
        """
        Carrega o conteúdo dos arquivos de vários formatos.

        :return: Lista de conteúdos de arquivos.
        """
        try:
            documents = []

            for file in os.listdir(file_path):
                
                _file_path = os.path.join(file_path, file)

                if file.endswith('.pdf'):
                    loader = PyMuPDFLoader(_file_path)
                elif file.endswith('.txt'):
                    loader = TextLoader(_file_path)
                elif file.endswith('.csv'):
                    loader = CSVLoader(_file_path)
                else:
                    loader = UnstructuredFileLoader(_file_path)

                documents.extend(loader.load())

            return documents
        except Exception as e:
            print(f"Erro ao carregar os arquivos: {e}")
            return []

    def split_docs(self, documents: List[str]):
        """
        Divide os documentos fornecidos em chunks após tokenizá-los com TikToken.

        :param documents: Lista de documentos a serem divididos.
        :return: Chunks dos documentos.
        """
        # Carregar o codificador para o modelo específico
        encoding = tiktoken.get_encoding("cl100k_base")  # Substitua 'cl100k_base' pelo codificador apropriado

        for doc in documents:
            doc_content = self.normalize_text(getattr(doc, 'page_content'))
            # Tokenizar o conteúdo do documento
            tokens = encoding.encode(doc_content)
            # Decodificar os tokens de volta para string (opcional, dependendo de como você quer processar)
            doc_content = encoding.decode(tokens)
            doc.page_content = doc_content

        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,  # Tamanho do chunk aumentado para capturar mais contexto
                chunk_overlap=20  # Sobreposição para manter a continuidade do contexto entre chunks
            )
            
            chunks = text_splitter.split_documents(documents)
            return chunks
        
        except Exception as e:
            print(f"Erro ao dividir documentos: {e}")
            return None