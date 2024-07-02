import requests, json
from openai import OpenAI
from assistant.models import ChatGPTModels, OllamaModels

client = OpenAI(api_key="")

def chatgpt_request(prompt:str, content:str, model:str=ChatGPTModels.GPT_4o) -> str:
  response = client.chat.completions.create(
    model=model,
    response_format={"type": "text"},
    messages=[
      {"role": "system", "content": prompt },
      {"role": "user", "content": content }
    ]
  )
  return response.choices[0].message.content

def ollama_request(prompt:str, content:str, model:str=OllamaModels.LLAMA3_8B_latest) -> str:
    url = "http://192.168.1.6:11434/api/chat"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "model": model,
        "messages": [
            { "role": "system", "content": prompt },
            { "role": "user", "content": content }
        ],
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        response_data = response.json()
        print(response_data)
        return response_data['message']['content']
    else:
        return {"error": f"Request failed with status code {response.status_code}"}