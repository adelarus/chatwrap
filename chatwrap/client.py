#Sends requests to LLM
import json
import requests
import diskcache as dc
import hashlib

def cache_request(funct):
    def wrapper(*args, **kwargs):
        cache = dc.Cache('cache')
        # generate the key as a has of the prompt
        print(f'Args: {args}')
        key = hashlib.sha256(args[1].encode()).hexdigest()
        print(f'Key: {key}')
        if key in cache:
            print('Cache hit')
            return cache[key]
        else:
            print('Cache miss')
            result = funct(*args, **kwargs)
            cache[key] = result
            return result
    return wrapper

class LLMClient:
    '''
    text
    Connect to LLM sever
    send request to LLM server
    '''

    totalNoOfTokens = 0
    
    def __init__(self, url, openai_key):
        self.openai_key = openai_key

        self.url = url

        print(f'Connecting to {self.url}')

        response = requests.get(f'{self.url}/models')

        if response.status_code == 200:
            print('Connected to LLM')

            models = response.json()

            #print(f'Available models: {models}')


    def log_tokens(funct):
        def wrapper(*args, **kwargs):
           
            result = funct(*args, **kwargs)
  
            total_tokens = result.get('usage', {}).get('total_tokens', 0)

            LLMClient.totalNoOfTokens += total_tokens

            print(f'Total tokens used: {total_tokens}')
 
            return result

        return wrapper

    #@log_tokens
    @cache_request
    def send_request(self, prompt, model="4o-mini", temperature=0.7, streaming=False,
                     system_prompt='You are a helpful HR assistant'):
        # body = {
        #     "model": model,
        #     "messages": [
        #     { "role": "system", "content": "" },
        #     { "role": "user", "content": prompt }
        #     ],
        #     "temperature": temperature,
        #     "max_tokens": 100,
        #     "stream": streaming
        # }
        body = {"model": "gpt-4o",
               "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content":prompt}
                ]}
        headers = {
           "Content-Type": "application/json",
           "Authorization": "Bearer " + self.openai_key
        }
       
        response = requests.post(f'{self.url}', json=body, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            message_content = response_json.get('choices', [{}])[0].get('message', {}).get('content', 'No content')
            
            print(f"Response*: {message_content}")
           
        else:
            print(f'Error: {response.status_code}')
    
        return json.loads(message_content)