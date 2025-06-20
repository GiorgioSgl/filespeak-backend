import chromadb
from decouple import config
import chromadb.utils.embedding_functions as embedding_functions

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=config("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

client = chromadb.Client()
collection = client.create_collection("sample_collection", embedding_function=openai_ef)