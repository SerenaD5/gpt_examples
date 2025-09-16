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

