## BELOW IS MODIFIED FROM OPENAI SDK TEMPLATE, adapted to ARK.
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

# Make sure the environment variable ARK_API_KEY is set.

# Call the openai ChatCompletion endpoint, with th ChatGPT model
response = client.chat.completions.create(model="doubao-seed-1-6-thinking-250715", #kimi-k2-250905
messages=[
      {"role": "user", "content": "Hello World!"}
  ])

# Extract the response
print(response.choices[0].message.content)

## BELOW FROM ARK SDK TEMPLATE. 
# import os
# from openai import OpenAI

# # 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# # 初始化Openai客户端，从环境变量中读取您的API Key
# client = OpenAI(
#     # 此为默认路径，您可根据业务所在地域进行配置
#     base_url="https://ark.cn-beijing.volces.com/api/v3",
#     # 从环境变量中获取您的 API Key
#     api_key=os.environ.get("ARK_API_KEY"),
# )

# # Non-streaming:
# print("----- standard request -----")
# completion = client.chat.completions.create(
#     # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
#     model="kimi-k2-250905",
#     messages=[
#         {"role": "system", "content": "你是人工智能助手"},
#         {"role": "user", "content": "你好"},
#     ],
# )
# print(completion.choices[0].message.content)

# # Streaming:
# print("----- streaming request -----")
# stream = client.chat.completions.create(
#     # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
#     model="kimi-k2-250905",
#     messages=[
#         {"role": "system", "content": "你是人工智能助手"},
#         {"role": "user", "content": "你好"},
#     ],
#     # 响应内容是否流式返回
#     stream=True,
# )
# for chunk in stream:
#     if not chunk.choices:
#         continue
#     print(chunk.choices[0].delta.content, end="")
# print()