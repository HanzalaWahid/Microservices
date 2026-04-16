
from groq import Groq

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

key = GROQ_API_KEY


def analyze_code_with_llm(file_content , file_name):
    prompt = f""" 
    Analyze the following code for:
    - Code style and formatting issues
    - Potential Bugs and errors
    - Performance Improvements
    - Best Practices
        
    
    File: {file_name}
    Content : {file_content}
                

Provide a detailed JSON output with the structure 
            {{
                "issue":[
                {{
                "type" : "<styling|bugs|performance|best practice>",
                "line" : "line_number",
                "description": "<description>",
                "suggestion" : "<suggestion>"
                }}
                ]
                }}

                
``` json
    """

    client = Groq(api_key=key)
    completion = client.chat.completions.create( model = "llama3-8b-8192", messages = [
        {
            "role" : "user",  
            "content" : prompt 
        }
    ],  
        temperature = 1,
        top_p = 1 ,

    )

    print(completion.choices[0].message.content )


# file_path = r"C:\Users\kk\Desktop\python\Python_microservices\fastapi_app\main.py"  
# with open(file_path, "r", encoding="utf-8") as f:
#     content = f.read()

# print(analyze_code_with_llm(content, file_path))
