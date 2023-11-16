from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import MongoDBAtlasVectorSearch
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


import os

DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

uri = "mongodb+srv://yvesatsaporous:" + DATABASE_PASSWORD + "@cluster0.qtil59y.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

DB_NAME = "langchain_db"
COLLECTION_NAME = "test"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "default"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=0
)

loader = TextLoader("facts.txt")
docs = loader.load_and_split(
    text_splitter=text_splitter
)

chat = ChatOpenAI(verbose=True)
embeddings = OpenAIEmbeddings()
# db = Chroma(
#     docs,
#     persist_directory="emb",
#     embedding_function=embeddings
# )
# retriever = db.as_retriever()

vector_search = MongoDBAtlasVectorSearch.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(disallowed_special=()),
    collection=MONGODB_COLLECTION,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)

retriever = vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 100, "post_filter_pipeline": [{"$limit": 25}]},
)

chain = RetrievalQA.from_chain_type(
    llm=chat,
    retriever=retriever,
    chain_type="stuff"
)
print("Here")

query = "What is an interesting fact about Golf"

results = vector_search.similarity_search_with_score(
    query=query,
    k=5,
)

for result in results:
    print("\n")
    print(result.page_content)


result = chain.run("What is an interesting fact about Golf")

print(result)
