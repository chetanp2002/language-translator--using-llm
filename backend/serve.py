from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

# Initialize model
model = ChatGroq(model='gemma2-9b-it', groq_api_key=groq_api_key)

# Prompt template
system_template = "Translate the following into {language}"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template), 
    ('user', '{text}')
])

parser = StrOutputParser()
chain = prompt_template | model | parser

# FastAPI App
app = FastAPI(title='Langchain Server', description="API server using Langchain and FastAPI")

# Input Schema
class TranslationInput(BaseModel):
    language: str
    text: str

@app.post('/chain/invoke')
async def invoke_chain(input: TranslationInput):
    data = {"language": input.language, "text": input.text}
    response = chain.invoke(data)
    return {"response": response}

# Add routes for LangServe
add_routes(app, chain, path='/chain')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
