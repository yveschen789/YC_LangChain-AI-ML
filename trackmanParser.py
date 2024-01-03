from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import argparse
import json
import os

from helpers import HelperClass

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--task", default="get values for ClubpPath")
#parser.add_argument("--values", default="json")

max_tokens = 4097

DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

uri = "mongodb+srv://yvesatsaporous:" + DATABASE_PASSWORD + "@cluster0.qtil59y.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))


DB_NAME = "langchain_db"
COLLECTION_NAME = "trackmandata"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "default"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

llm = OpenAI()

#get json in memory
file_path = 'testtrackmanreportingfitting.json'
json_object = HelperClass.load_json_file(file_path)

parser.add_argument("--values", default=json.dumps(json_object))

parser.add_argument("--statisticalValue", default="Maxval")

args = parser.parse_args()

print(json_object)
code_prompt = PromptTemplate(
    input_variables=["task", "values"],
    template="parse this {values} document for {task}."
)
test_prompt = PromptTemplate(
    input_variables=["statisticalValue", "result"],
    template="find the {statisticalValue} in data\n{result}"
)

code_chain = LLMChain(
    llm=llm,
    prompt=code_prompt,
    output_key="result"
)
test_chain = LLMChain(
    llm=llm,
    prompt=test_prompt,
    output_key="whatever"
)

chain = SequentialChain(
    chains=[code_chain, test_chain],
    input_variables=["task", "values", "statisticalValue"],
    output_variables=["result", "whatever"]
)

result = chain({
    "values": args.values,
    "task": args.task,
    "statisticalValue": args.statisticalValue
})

#log some statistics before putting into db
print(">>>>>> GENERATED RESULTS:")
print(result["result"])

MONGODB_COLLECTION.insert_one(result["result"])

print(">>>>>> GENERATED STATISTIC:")
print(result["whatever"])
