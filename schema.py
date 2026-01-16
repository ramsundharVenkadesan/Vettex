from pydantic import BaseModel, Field # Import classes from Pydantic library to define, format, and validate data
from typing import List # Import List class from Typing package

class Source(BaseModel): # This class is designed to represent a single reference link used by the agent.
    """Schema for a source used by an agent"""
    url:str = Field(description="URL of the source")

class AgentResponse(BaseModel): # This class structures the "final answer" from a research agent, breaking it down into specific technical categories
    """Schema for agent response with answer and sources"""
    value_proposition_analysis:str = Field(description="A summary of what the company claims vs what their tech supports")
    technical:str = Field(description="Is it proprietary code, an unique dataset, or wrapper?")
    developer_sentiment:str = Field(description="What the engineering community states about their tech?")
    red_flags:List[str] = Field(description="Any potential issues or concerns", default_factory=list)
    verdict:str = Field(description="The final verdict from a technical perspective")
    sources:List[str] = Field(description="A list of full, valid web URLs (starting with http:// or https://) used in the research. Do not include placeholder text.", default_factory=list)