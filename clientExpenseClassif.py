import os
from groq import Groq
import json

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

prompt = """
Below are transactions in JSON format. Each JSON object is one transaction. Each transaction has a description. Use the description to put each transaction into expense categories. All transactions are in GBP (£). 
Here are the transactions below:
"""
output = []

with open('/Users/sishirsirugudi/MK Intern Stuff/HSBCStatementJSON.txt', "r") as file:
    data = json.load(file)  
    file_content = json.dumps(data, indent=2)  
    fullPrompt = prompt + file_content

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": fullPrompt,  
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    output.append(chat_completion.choices[0].message.content)
    print(chat_completion.choices[0].message.content)

with open('/Users/sishirsirugudi/MK Intern Stuff/HSBCStatementClassifiedExpense.txt', "w") as file:
    file.write(chat_completion.choices[0].message.content)
