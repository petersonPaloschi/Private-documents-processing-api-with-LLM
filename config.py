import warnings
from platform import python_version

warnings.filterwarnings("ignore")
#os.system('cls')
print(f'Este projeto foi desenvolvido na versão do Python 3.12.1, sua versão atual do Python é a {python_version()}')

# Configurações do Hugging Face
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'  # https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
DEVICE = 'cpu'

#OpenAI
OPENAI_API_KEY= 'YOUR_API_KEY'
OPENAI_LLM_MODEL = 'gpt-4o' #'GPT-3.5-TURBO'

#AzureOpenAI
AZURE_OPENAI_ENDPOINT = "YOUR_ENDPOINT"
AZURE_OPENAI_API_KEY = "YOUR_API_KEY"
AZURE_OPENAI_API_VERSION = "2024-02-01"
AZURE_OPENAI_MODEL = "gpt-4o"
AZURE_OPENAI_MODEL_NAME = AZURE_OPENAI_MODEL
AZURE_OPENAI_MAX_TOKENS = 1000

# Caminho para o vetor de armazenamento
PATH_VECTOR_STORE = 'files/vectorstore'
PATH_FILE = 'files/docs'

DEBUG = True