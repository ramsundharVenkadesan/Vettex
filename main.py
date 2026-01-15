from fastapi import FastAPI, Request, Form
from dotenv import load_dotenv # Import function to load environment variables


from langchain_classic.agents import AgentExecutor # Import system to execute tools
from langchain_classic.agents.react.agent import create_react_agent # Import function to create a react agent

from langchain_google_genai import ChatGoogleGenerativeAI # Import the LLM that will be used by the agent
from langchain_tavily import TavilySearch # Import LangChain integrated Tavily search

from langchain_core.prompts import PromptTemplate # Import the PromptTemplate class to format the prompt
from langchain_core.runnables import RunnableLambda # Import the RunnableLambda class to create Runnable objects

from langchain_core.output_parsers.pydantic import PydanticOutputParser # LangChain output parser that takes in the response from LLM that will parsed into Pydantic model object

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS # Import the react prompt that will be sent to LLM
from schema import AgentResponse # Import the Pydantic data-class that agent uses to format final output

from pydantic import BaseModel, Field
from starlette import status

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

load_dotenv() # Load the environment variables
app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_agent():
    tools = [TavilySearch()]  # Register the TavilySearch instance as a tool that the LLM can invoke
    llm = ChatGoogleGenerativeAI(
        model='gemini-3-flash-preview')  # LLM model using Google Gemini, optimized for fast responses
    output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
    promptTemplate = PromptTemplate(template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS, input_variables=["tools", "input", "tool_names", "agent_scratchpad"]).partial(format_instructions=output_parser.get_format_instructions())
    agent = create_react_agent(llm=llm, tools=tools, prompt=promptTemplate)
    executor = AgentExecutor(agent=agent, verbose=True, tools=tools, handle_parsing_errors=True)
    extract_output = RunnableLambda(lambda x: x['output'])
    parse_output = RunnableLambda(lambda x: output_parser.parse(x))
    chain = executor | extract_output | parse_output
    return chain


class CompanyInput(BaseModel):
    company_name: str = Field(description="Name of the company to search for", min_length=1)
    url:str = Field(description="URL of the company's website")


@app.get("/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def analyze(request:Request, company_name:str=Form(...), url:str=Form(...)):
    task_description = (
        f"Perform a technical due diligence analysis on {company_name}. "
        f"Start by visiting their website at {url}."
    )
    result = get_agent().invoke({"input": task_description})
    return templates.TemplateResponse("report.html", {"request": request, "company_name": company_name, "data": result})