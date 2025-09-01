import os
from groq import Groq
import json

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

prompt = """
Below is a bank statement. Ignore all text that is not in the transaction table. Extract all the transaction information and put each transaction in a JSON format.
The position of the text is preserved as it would appear in the original document.
The table for the transactions are in columns. Each column should be a separate field in the JSON.
If there are no transactions in the page then ignore it and do nothing.
Analyze the provided text. Find out individual transactions.


The line may have values missing in 'Money In' or 'Money Out', but at least one value and the balance is always present. If any field has missing values then still include the field and keep the value empty. There may also be the same description for multiple lines. This is correct do not skip the line out.

Only give the JSON object without any additional text or explanation.
Here are the transactions:
"""

with open('/Users/sishirsirugudi/MK Intern Stuff/testinggg.txt', "r") as file:
    lines = file.readlines() 

cleanedLines = []
output = []

# I added a '§' betweem each page so that the statement to passed by page into the LLM.
# This is becuase the LLM does not have a large enough context size for the entire statement
for line in lines:
    if "§" in line:
        # Process the current chunk if it has content
        if cleanedLines:
            transactions = "\n".join(cleanedLines)
            fullPrompt = prompt + transactions
            
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
            
        # Reset for next chunk
        cleanedLines = []
    
    elif line.strip():  
        cleanedLines.append(line.strip())  

# Process the final chunk if it exists (in case file doesn't end with §)
if cleanedLines:
    transactions = "\n".join(cleanedLines)
    fullPrompt = prompt + transactions
    
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

with open ('/Users/sishirsirugudi/MK Intern Stuff/lloydsStatementJSON.txt', 'w') as file:
    for j in output:
        file.write(j+'\n')

