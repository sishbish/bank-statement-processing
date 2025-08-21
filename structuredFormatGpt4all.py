from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_community.llms import GPT4All
from langchain.schema.runnable import RunnableSequence
from pydantic import BaseModel, Field
from typing import List, Literal
import json
import time, psutil, os


class Transaction(BaseModel):
    Date: str = Field(description = "Date of transaction in DD/MM/YYYY format")
    Description: str = Field(description = "Transaction description")
    Type: Literal[
        "BCG", "BP", "CHG", "CHQ", "COR", "CPT", "DD", "DEB", "DEP", "FEE",
        "FPI", "FPO", "MPI", "MPO", "PAY", "SO", "TFR"
    ] = Field(description="Transaction type code (must be one of the listed codes)")
    Money_In: str = Field(default = "", description = "Amount of money coming in (£), empty if not applicable")
    Money_Out: str = Field(default = "", description = "Amount of money going out (£), empty if not applicable")
    Balance: str = Field(description = "Net balance of bank account")

class TransactionList(BaseModel):
    transactions: List[Transaction]

parser = PydanticOutputParser(pydantic_object=TransactionList)
model = GPT4All(model='/Users/sishirsirugudi/Library/Application Support/nomic.ai/GPT4All/Meta-Llama-3-8B-Instruct.Q4_0.gguf', verbose=True)
parser = OutputFixingParser.from_llm(parser=parser, llm=model)

prompt = PromptTemplate(
    template = """
Below are transaction lines from a bank statement in plain text format.
The position of the text is preserved as it would appear in the original document.
Analyze the provided text. Find out individual transactions.
Each line represents one transaction, and columns appear in this order:
Date  
Description   
Type   
Money In (£)  
Money Out (£)  
Balance (£)

The line may have values missing in 'Money In' or 'Money Out', but at least one value and the balance is always present. There may also be the same description for multiple lines. This is correct do not skip the line out.

Extract the transaction lines into a JSON object containing a list called "transactions" following this format:
{format_instructions}
ONLY extract transactions exactly as they appear. Do NOT create or invent any transaction data.

Transaction line:
{transaction_line}

Only give the JSON object without any additional text or explanation.
""",
    input_variables=["transaction_line"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = RunnableSequence(prompt, model)

process = psutil.Process(os.getpid())
start_time = time.time()
responses = []



with open('/Users/sishirsirugudi/MK Intern Stuff/lloydsStatementShort.txt', "r") as file:
    while True:
        lines = [file.readline() for _ in range(3)]
        lines = [l for l in lines if l]
        if not lines:
            break

        chain_input = "\n".join(lines)
        print(f"Processing lines:\n{chain_input}\n")
        try:
            output = chain.invoke({"transaction_line": chain_input})
            parsed_transactions = parser.parse(output)
            print(parsed_transactions.dict())
            responses.append(parsed_transactions.dict())
        except Exception as e:
            print("Parsing Error:", e)
            print(output)

all_transactions = [transaction for response in responses for transaction in response["transactions"]]

print(json.dumps({"transactions": all_transactions}, indent=2))

end_time = time.time()
print(f"\n⏱️ Total execution time: {end_time - start_time:.2f} seconds")
print(f"Max memory usage: {process.memory_info().rss / 1024**2:.2f} MB")
