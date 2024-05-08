from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values(".env")
CHATGPT_API_KEY = config["CHATGPT_API_KEY"]


CHATGPT_KEY = CHATGPT_API_KEY
client = OpenAI(api_key=CHATGPT_KEY)

# prompt = "На основі назви товару [назва товару] виділи 5 релевантних товарів з списку. Список: [товар1, товар2, товар3, товарN]. У відповіді поверни тільки 5 товарів і нічого зайвого."
prompt = "Using name of product: [назва товару] create list of most relevant products. List: [товар1, товар2, товар3, товарN]. In response add only list with products, and nothing else."

completion = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  messages=[
    # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."}
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices)
print("---------------------------------")
print(completion.choices[0].message)