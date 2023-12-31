from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate, HumanMessagePromptTemplate,ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationSummaryMemory, FileChatMessageHistory
import argparse
import time

from helpers import HelperClass

parser = argparse.ArgumentParser()
parser.add_argument("--task", default="return a list of random numbers")
parser.add_argument("--language", default="python")
args = parser.parse_args()

#prewritten lines will not be used by the ChatOpenAI model
lines_array = HelperClass.read_file_into_array("inputvals.txt")

#-------------------------------------------------------------------------------------------

#CHAT
llm = ChatOpenAI(verbose=True)

memory = ConversationSummaryMemory(
    # chat_memory=FileChatMessageHistory("messages.json"),
    memory_key="messages",
    return_messages=True,
    llm=llm
)


# code_prompt = PromptTemplate(
#     input_variables=["task", "language"],
#     template=lines_array[0]
# )
# test_prompt = PromptTemplate(
#     input_variables=["language", "code"],
#     template=lines_array[1]
# )
prompt = ChatPromptTemplate(
    input_variables=["input", "messages"],
    messages = [
    MessagesPlaceholder(variable_name="messages"),
    HumanMessagePromptTemplate.from_template("{input}")
]
)

# code_chain = LLMChain(
#     llm=llm,
#     prompt=prompt,
#     output_key="code"
# )
# test_chain = LLMChain(
#     llm=llm,
#     prompt=test_prompt,
#     output_key="test"
# )

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    verbose=True
)

# chain = SequentialChain(
#     chains=[code_chain, test_chain],
#     input_variables=["task", "language"],
#     output_variables=["test", "code"]
# )
while True:
    content = input(">> ")
    if content == "quit":
        break

    result = chain({
        "input" : content
    })
    print(result["text"])


    time.sleep(2.4)