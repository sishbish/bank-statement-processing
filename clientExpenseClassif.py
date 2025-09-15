import os
from groq import Groq
import json

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# ------------- old prompt without transaction amount: -------------
# # You are a financial categorization assistant. Below are bank transactions in JSON format where each transaction is a separate JSON object.

# Your task:
# 1. Categorize each transaction by expense type based on the description
# 2. Create separate JSON objects for each expense category
# 3. Within each category, include all transactions that belong to that category
# 4. Each transaction should be identified by its description from the input

# Expense categories to use:
# - Food & Dining (restaurants, groceries, food delivery, cafes)
# - Transportation (fuel, public transport, parking, car maintenance, taxi/uber)
# - Subscriptions (streaming services, software, gym memberships, recurring services)
# - Household Bills (utilities, rent/mortgage, insurance, internet, phone)
# - Shopping (retail purchases, clothing, electronics, general merchandise)
# - Entertainment (movies, games, events, hobbies)
# - Healthcare (medical expenses, pharmacy, doctor visits)
# - Travel (hotels, flights, vacation expenses)
# - Education (courses, books, educational materials)
# - Other (uncategorized expenses)

# Output format:
# Create a JSON object for each category that contains transactions. Use this structure:
# {
#   "category_name": "Food & Dining",
#   "transactions": [
#     "TESCO STORES 1234",
#     "MCDONALDS RESTAURANT",
#     "DELIVEROO ORDER"
#   ]
# }

# If a category has no transactions, do not include it in the output.

# IMPORTANT: Output ONLY the JSON objects. Do not include any explanations, text, or additional content. Start your response directly with the JSON.

# All transactions are in GBP (£). 
# Here are the transactions below:

# --------------------------------------

prompt = """
You are a financial categorization assistant. Below are bank transactions in JSON format where each transaction is a separate JSON object.

Your task:
1. Categorize each transaction by expense type based on the description
2. Create separate JSON objects for each expense category
3. Within each category, include all transactions that belong to that category
4. Each transaction should be identified by its description from the input

Expense categories to use:
- Food & Dining (restaurants, groceries, food delivery, cafes)
- Transportation (fuel, public transport, parking, car maintenance, taxi/uber)
- Subscriptions (streaming services, software, gym memberships, recurring services)
- Household Bills (utilities, rent/mortgage, insurance, internet, phone)
- Shopping (retail purchases, clothing, electronics, general merchandise)
- Entertainment (movies, games, events, hobbies)
- Healthcare (medical expenses, pharmacy, doctor visits)
- Travel (hotels, flights, vacation expenses)
- Education (courses, books, educational materials)
- Other (uncategorized expenses)

Output format:
Create a JSON object for each category that contains transactions. Use this structure:
{
  "category_name": "Food & Dining",
  "transactions": [
    {
      "description": "TESCO STORES 1234",
      "amount": "25.50"
    },
    {
      "description": "MCDONALDS RESTAURANT", 
      "amount": "8.99"
    }
  ]
}

For each transaction, include:
- "description": The transaction description from the input
- "amount": The actual monetary value from either "Money In" or "Money Out" field (whichever has a value)

If a category has no transactions, do not include it in the output.

IMPORTANT: Output ONLY the JSON objects. Do not include any explanations, text, or additional content. Start your response directly with the JSON.

All transactions are in GBP (£). 
Here are the transactions below:
"""
output = []

with open('extracted JSONs/NK.json', "r") as file:
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

with open('expense classification/NK.txt', "w") as file:
    file.write(chat_completion.choices[0].message.content)
