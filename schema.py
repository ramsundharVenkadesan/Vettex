from pydantic import BaseModel, Field
from typing import List

class AgentResponse(BaseModel):
    value_proposition_analysis:str = Field(description="A summary of what the company claims vs what their tech supports")
    technical:str = Field(description="Is it proprietary code, an unique dataset, or wrapper?")
    developer_sentiment:str = Field(description="What the engineering community states about their tech?")
    red_flags:List[str] = Field(description="Any potential issues or concerns")
    verdict:str = Field(description="The final verdict from a technical perspective")