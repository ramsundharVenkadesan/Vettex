from dotenv import load_dotenv # Import function to load environment variables
import os, certifi # Import package to interact with Operating System (OS) and provide a collection of Root Certificates to connect to websites or APIs
import asyncio # Import engine that allows code to perform multiple tasks at once
import json # Import package to convert dictionaries into JSON strings for front-end processing

from agent import get_agent # Import the AI agent

from pydantic import BaseModel, Field # Import classes from Pydantic library to define, format, and validate data
from starlette import status # Import a library of human-readable HTTP codes

from fastapi.templating import Jinja2Templates # Import engine to handle HTML files
from fastapi import FastAPI, Request, Form # Import classes from FastAPI library required to create a web server and handle requests or input data
from fastapi.responses import HTMLResponse, StreamingResponse # Import different response types to render webpages and real-time outputs
from langchain_core.callbacks.base import AsyncCallbackHandler # Import base-class required to "eavesdrop" on the AI agent's actions

os.environ['SSL_CERT_FILE'] = certifi.where() # Guides the program to find the "list of trusted sources" when it tries to connect to a website or an API securely
load_dotenv() # Load the environment variables

app = FastAPI() # Initialize FastAPI application
templates = Jinja2Templates(directory="templates") # Initialize Jinja2Templates to render HTML files located in Templates directory

class WebStreamCallbackHandler(AsyncCallbackHandler): # A class that inherits from AsyncCallbackHandler which allows it to hook into LangChain's asynchronous events

    def __init__(self, queue): # Constructor that accepts a queue
        self.queue = queue # Store the queue object so that handler can push messages into as the agent works

    async def on_agent_action(self, action, **kwargs): # Method is triggered every time LLM decides to use a tool
        if "Action:" in action.log: # Check if raw output from LLM contains the string "Action"
            parts = action.log.split("Action:") # Split the string into two parts based on the "Action" substring
            thought = parts[0].replace("Thought:", "").strip() # Clean up the first part by removing "Thought" prefix

            if thought: # A valid thought string is pushed into queue with prefix
                await self.queue.put(f"THOUGHT: {thought}")

            await self.queue.put(f"ACTION: Invoking {action.tool} with input {action.tool_input}") # Pushes clean, readable message into the queue identifying which tool is being used
        else: # LLM output does not follow the "Action:" format
            await self.queue.put(f"LOG: {action.log.strip()}") # Raw log is sent to the queue so information is lost

    async def on_tool_end(self, output, **kwargs): # Method triggered automatically after a tool finishes executing
        await self.queue.put(f"OBSERVATION: Data retrieved successfully.") # Capture that a tool finished



class CompanyInput(BaseModel): # Data-Class to store company name and URL
    company_name: str = Field(description="Name of the company to search for", min_length=1, max_length=100) # Company name field
    url:str = Field(description="URL of the company's website", min_length=4, max_length=200) # URL of the company's website'


@app.get("/", status_code=status.HTTP_200_OK, response_class=HTMLResponse) # Handle GET requests sent to roor URL and set response code 200
async def index(request:Request): # Asynchronous Function to render the index.html file
    return templates.TemplateResponse("index.html", {"request": request}) # Prompt Jinja2Templates to find and render the HTML file

@app.post("/", status_code=status.HTTP_200_OK, response_class=HTMLResponse) # Handle POST requests that contains user input
async def analyze(request:Request, company_name:str=Form(...), url:str=Form(...)): # Function that extracts company name and URL from HTML form fields
    input_data = CompanyInput(company_name=company_name, url=url) # Pass the arguments and validate them using a Pydantic model

    async def event_generator(): # Inner function to create a persistent connection they stays open so the server can push updates to brower as they happen
        queue = asyncio.Queue() # Temporary area for holding messages
        handler = WebStreamCallbackHandler(queue) # Listens to AI agents to put "Thought" and "Action" into the queue
        task_description = f"Perform technical due diligence on {input_data.company_name} at {input_data.url}." # Input to Agent

        agent_task = asyncio.create_task(get_agent().ainvoke({"input": task_description}, config={"callbacks": [handler]})) # Start AI agent in the background

        while (not agent_task.done()) or (not queue.empty()): # Keep the loop running as long as the agent is working or there are messages in the queue not sent to the user
            try: # Try code block for erroneous code
                msg = await asyncio.wait_for(queue.get(), timeout=0.2) # Attempt to grab message from queue
                yield f"data: {json.dumps({'type': 'log', 'content': msg})}\n\n" # Send packets of data to the browser without closing connection (Server-Sent Events (SSE))
            except asyncio.TimeoutError: # No new messages arrived in the queue for 200ms
                continue # Loops goes back to the top and tries again

        result = await agent_task # Wait for the agent to provide final answer
        final_html = templates.get_template("report.html").render({ "request": request, "company_name": company_name, "data": result}) # Render the report HTML page using agent data
        yield f"data: {json.dumps({'type': 'final', 'content': final_html})}\n\n" # Send the final, formatted HTML report to the browser

    return StreamingResponse(event_generator(), media_type="text/event-stream") # Allows FastAPI to keep the HTTP connection open and use event-generator to feed data to the user bit-by-bit
