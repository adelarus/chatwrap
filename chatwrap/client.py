#Sends requests to LLM
import json
import requests

class LLMClient:
    '''
    text
    Connect to LLM sever
    send request to LLM server
    '''

    totalNoOfTokens = 0
    
    def __init__(self, url):

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
    def send_request(self, prompt, model="4o-mini", temperature=0.7, streaming=False):
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
        body = {"model": "gpt-4o",  # using the 4o-mini model
               "messages": [
                    {"role": "system", "content": '''You are a helpful HR assistant.
                      Your job is to extract the technical skills and the years of experience in each skill from the CV provided by the user.
                      Please format the output to a JSON list of skills.
                      Please do not output markdown content.'''},
                    {"role": "user", "content":prompt}
                ]}
        headers = {
           "Content-Type": "application/json",
           "Authorization": "Bearer KEY" 
        }
       
        response = requests.post(f'{self.url}', json=body, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            message_content = response_json.get('choices', [{}])[0].get('message', {}).get('content', 'No content')
            
            print(f"Response*: {message_content}")
           
        else:
            print(f'Error: {response.status_code}')
    
        return json.loads(message_content)