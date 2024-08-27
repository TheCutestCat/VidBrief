from pydantic import BaseModel,Field

class Highlits(BaseModel):
    text: str
    end_time: str 

class HighlitsResponseFromat(BaseModel):
    highlits : list[Highlits]


HighlitsPrompts = """
Select up to 15 highlights from the input subtitles. 
Ensure each text description is precise, with no more than 30 words. 
The corresponding 'end_time' should be accurate to the millisecond.as
"""