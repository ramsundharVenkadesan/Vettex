from fastapi import FastAPI, Request, Form
from dotenv import load_dotenv # Import function to load environment variables

import asyncio, json
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
from fastapi.responses import HTMLResponse, StreamingResponse
from langchain_core.callbacks.base import AsyncCallbackHandler

class WebStreamCallbackHandler(AsyncCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    async def on_agent_action(self, action, **kwargs):
        # Capture the Thought and Action
        thought = action.log.split("Action:")[0].strip()
        await self.queue.put(f"THOUGHT: {thought}")
        await self.queue.put(f"ACTION: Investigating via {action.tool}...")

    async def on_tool_end(self, output, **kwargs):
        # Capture that a tool finished
        await self.queue.put(f"OBSERVATION: Data retrieved successfully.")

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
    async def event_generator():
        queue = asyncio.Queue()
        handler = WebStreamCallbackHandler(queue)
        task_description = f"Perform technical due diligence on {company_name} at {url}."

        # Start agent in background
        agent_task = asyncio.create_task(
            get_agent().ainvoke({"input": task_description}, config={"callbacks": [handler]})
        )

        # 1. Stream the logs as they happen
        while not agent_task.done() or not queue.empty():
            try:
                msg = await asyncio.wait_for(queue.get(), timeout=0.2)
                yield f"data: {json.dumps({'type': 'log', 'content': msg})}\n\n"
            except asyncio.TimeoutError:
                continue

        # 2. Stream the final HTML report
        result = await agent_task
        final_html = templates.get_template("report.html").render({
            "request": request, "company_name": company_name, "data": result
        })
        yield f"data: {json.dumps({'type': 'final', 'content': final_html})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")