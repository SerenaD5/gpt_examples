from dotenv import load_dotenv

load_dotenv()
from intentservice import IntentService
from responseservice import ResponseService
from dataservice import DataService

# Example pdf
pdf = 'files/ExplorersGuide.pdf'

data_service = DataService()

# Drop all data from redis if needed
data_service.drop_redis_data()

# Load data from pdf to redis
data = data_service.pdf_to_embeddings(pdf)

data_service.load_data_to_redis(data)

intent_service = IntentService()
response_service = ResponseService()

# Question 
question = 'Where to find treasure chests?'
# Get the intent
intents = intent_service.get_intent(question)
# Get the facts # 当用户提问时，通过搜索获取相关数据
facts = data_service.search_redis(intents) # 这里使用了存储的数据
# Get the answer
answer = response_service.generate_response(facts, question)
print(answer)
