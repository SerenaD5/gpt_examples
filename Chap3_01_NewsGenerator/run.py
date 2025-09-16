## BELOW IS MODIFIED FROM OPENAI SDK TEMPLATE, adapted to ARK.
#doubao-seed-1-6-thinking-250715
from dotenv import load_dotenv

load_dotenv()
import os
from openai import OpenAI

# sometimes you may need to set up a proxy to access the API
# Make sure the environment variable PROXY_URL is set.
def build_http_client():
    '''
    Build an HTTP client with proxy settings from environment variables.
    Returns: httpx.Client: Configured HTTP client.
    '''
    import httpx
    timeout= httpx.Timeout(30.0, connect=10.0)
    try: 
        return httpx.Client(proxies = {
            "http://": os.environ.get("PROXY_URL", ""),
            "https://": os.environ.get("PROXY_URL", "")
        }, timeout=timeout)
    except TypeError: 
        transport = httpx.HTTPTransport(proxy=os.environ.get("PROXY_URL", ""))
        return httpx.Client(transport=transport, timeout=timeout)

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
    #add proxy if needed
    http_client=build_http_client()
)


from typing import List 


def ask_chatgpt(messages):
    response = client.chat.completions.create(model="doubao-seed-1-6-thinking-250715",
                                              messages=messages)
    return (response.choices[0].message.content)


prompt_role = '''You are an assistant for journalists. 
Your task is to write articles, based on the FACTS that are given to you. 
You should respect the instructions: the TONE, the LENGTH, and the STYLE'''


def assist_journalist(
        facts: List[str], # 这里指定 facts 参数是字符串列表
        tone: str, length_words: int, style: str):
    facts = ", ".join(facts)
    prompt = f'{prompt_role}\nFACTS: {facts}\nTONE: {tone}\nLENGTH: {length_words} words\nSTYLE: {style}'
    return ask_chatgpt([{"role": "user", "content": prompt}])


print(
    assist_journalist(
        ['The sky is blue', 'The grass is green'],
        'informal', 100, 'blogpost'))


# from typing import List
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI()


# def ask_chatgpt(messages):
#     response = client.chat.completions.create(model="gpt-3.5-turbo",
#                                               messages=messages)
#     return (response.choices[0].message.content)


# prompt_role = '''You are an assistant for journalists. 
# Your task is to write articles, based on the FACTS that are given to you. 
# You should respect the instructions: the TONE, the LENGTH, and the STYLE'''


# def assist_journalist(
#         facts: List[str],
#         tone: str, length_words: int, style: str):
#     facts = ", ".join(facts)
#     prompt = f'{prompt_role}\nFACTS: {facts}\nTONE: {tone}\nLENGTH: {length_words} words\nSTYLE: {style}'
#     return ask_chatgpt([{"role": "user", "content": prompt}])


# print(
#     assist_journalist(
#         ['The sky is blue', 'The grass is green'],
#         'informal', 100, 'blogpost'))
