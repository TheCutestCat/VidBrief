from pydantic import BaseModel,Field

class Highlits(BaseModel):
    text : str
    end_time : str

class SummaryResponseFromat(BaseModel):
    highlits : list[Highlits]


SummaryPrompts = """
I will provide a transcript of a video. Please summarize the content in a concise manner, ensuring that the key points and main ideas are clearly highlighted. The summary should be coherent and capture the essence of the video, aligned with the sequence of the transcript provided.

Input: video transcript
step 1 :
You should first find the highlits and its end_time. Please choose carefully, the quantity is best controlled within 5 pieces
"""