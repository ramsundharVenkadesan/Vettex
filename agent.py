from langchain_classic.agents import AgentExecutor # Import system to execute tools
from langchain_classic.agents.react.agent import create_react_agent # Import function to create a react agent

from langchain_google_genai import ChatGoogleGenerativeAI # Import the LLM that will be used by the agent
from langchain_tavily import TavilySearch # Import LangChain integrated Tavily search

from langchain_core.prompts import PromptTemplate # Import the PromptTemplate class to format the prompt
from langchain_core.runnables import RunnableLambda # Import the RunnableLambda class to create Runnable objects

from langchain_core.output_parsers.pydantic import PydanticOutputParser # LangChain output parser that takes in the response from LLM that will parsed into Pydantic model object

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS # Import the react prompt that will be sent to LLM
from schema import AgentResponse # Import the Pydantic data-class that agent uses to format final output


def get_agent():
    tools = [TavilySearch()]  # Register the TavilySearch instance as a tool that the LLM can invoke
    llm = ChatGoogleGenerativeAI(model='gemini-3-flash-preview')  # LLM model using Google Gemini, optimized for fast responses
    output_parser = PydanticOutputParser(pydantic_object=AgentResponse) # An instance of output-parser with the Pydantic class passed to the constructor

    promptTemplate = PromptTemplate( # Prompt template instance
                                    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS, # Template of the prompt with various placeholder/input variables
                                    input_variables=["tools", "input", "tool_names", "agent_scratchpad"] # A list of input variables in the template where data will be injected
                                    ).partial(format_instructions=output_parser.get_format_instructions()) # Partially populate the template with format instructions before executing

    agent = create_react_agent(llm=llm, tools=tools, prompt=promptTemplate) # Wire the LLM, registered tools, and prompt into a single chain (Runnable Object)

    executor = AgentExecutor(agent=agent, tools=tools, # Wraps the ReAct chain and tools into a logic loop (Agent Runtime)
                             verbose=True, handle_parsing_errors=True) # Enable debugging and gracefully handle any parsing errors

    extract_output = RunnableLambda(lambda x: x['output']) # Transform the input dictionary to extract value of output key
    parse_output = RunnableLambda(lambda x: output_parser.parse(x)) # Invoke the parse method on the input it gets

    chain = executor | extract_output | parse_output # Chain Workflow:
    # 1. Prompt passed to agent that outputs a response dictionary
    # 2. The dictionary is passed to the Runnable object that extracts value of output key
    # 3. Extracted value is passed to another Runnable object that parses the extracted value

    return chain # Return the final Runnable chain