
from groq import Groq

key = "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"


def analyze_code_with_llm(file_content , file_name):
    prompt = f""" 
    Analyze  the follwoing code for:
    - Code  style and formatting issue 
    -Potentail Bugs and error
    - Performance Improvement 
    - Best Practice
        
    
    File: {file_name}
    Content : {file_content}
                

Provide a detiled JSON output with the structure 
            {{
                "issue":[
                {{
                "type" : "<styling|bugs|performance|best practice>",
                "line" : "line_number",
                "description": "<description>",
                "sugggestion" : "<suggestion>"
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


file_path = r"C:\Users\kk\Desktop\python\Python_microservices\fastapi_app\main.py"  
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

print(analyze_code_with_llm(content, file_path))
