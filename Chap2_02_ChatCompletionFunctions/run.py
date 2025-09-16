# from dotenv import load_dotenv

# load_dotenv()
# from openai import OpenAI

# client = OpenAI()
# import json


# def find_product(sql_query):
#     # Execute query here
#     results = [
#         {"name": "pen", "color": "blue", "price": 1.99},
#         {"name": "pen", "color": "red", "price": 1.78},
#     ]
#     return results


# function_find_product = {
#         "name": "find_product",
#         "description": "Get a list of products from a sql query",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "sql_query": {
#                     "type": "string",
#                     "description": "A SQL query",
#                 }
#             },
#             "required": ["sql_query"],
#         },
#     }



# def run(user_question):
#     # Send the question and available functions to GPT
#     messages = [{"role": "user", "content": user_question}]

#     response = client.chat.completions.create(model="gpt-3.5-turbo-0613", messages=messages, tools=[{"type": "function", "function": function_find_product }])
#     response_message = response.choices[0].message

#     # Append the assistant's response to the messages
#     messages.append(response_message)
    

#     # Call the function and add the results to the messages
#     function_name = response_message.tool_calls[0].function.name
#     if function_name == "find_product":
#         function_args = json.loads(
#             response_message.tool_calls[0].function.arguments
#         )
#         products = find_product(function_args.get("sql_query"))
#     else:
#         # Handle error
#         products = []
#     # Append the function's response to the messages
#     messages.append(
#         {
#             "role": "tool",
#             "content": json.dumps(products),
#             "tool_call_id": response_message.tool_calls[0].id,
#         }
#     )
#     # Get a new response from GPT so it can format the function's response into natural language
#     second_response = client.chat.completions.create(model="gpt-3.5-turbo-0613",
#     messages=messages)
#     return second_response.choices[0].message.content


# print(run("I need the top 2 products where the price is less than 2.00"))


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

import json


def find_product(sql_query):
    # Execute query here
    results = [
        {"name": "pen", "color": "blue", "price": 1.99},
        {"name": "pen", "color": "red", "price": 1.78},
    ]
    return results


function_find_product = {
        "name": "find_product",
        "description": "Get a list of products from a sql query",
        "parameters": {
            "type": "object",
            "properties": {
                "sql_query": {
                    "type": "string",
                    "description": "A SQL query",
                }
            },
            "required": ["sql_query"],
        },
    }



def run(user_question):
    # Send the question and available functions to GPT
    messages = [{"role": "user", "content": user_question}]

    response = client.chat.completions.create(model="doubao-seed-1-6-thinking-250715", messages=messages, tools=[{"type": "function", "function": function_find_product }])
    response_message = response.choices[0].message
    print(response_message)
    print(response_message.tool_calls[0])
    # Append the assistant's response to the messages
    messages.append(response_message)
    

    # Call the function and add the results to the messages
    function_name = response_message.tool_calls[0].function.name
    if function_name == "find_product":
        function_args = json.loads(
            response_message.tool_calls[0].function.arguments
        )
        products = find_product(function_args.get("sql_query"))
    else:
        # Handle error
        products = []
    # Append the function's response to the messages
    messages.append(
        {
            "role": "tool",
            "content": json.dumps(products),
            "tool_call_id": response_message.tool_calls[0].id,
        }
    )
    # Get a new response from GPT so it can format the function's response into natural language
    second_response = client.chat.completions.create(model="doubao-seed-1-6-thinking-250715",
    messages=messages)
    print(second_response)
    return second_response.choices[0].message.content


print(run("I need the top 2 products where the price is less than 2.00"))
