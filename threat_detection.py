import boto3
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def threaten_detection(context, conversation):
    bedrock_client = boto3.client('bedrock-runtime', 
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN')
    )

    prompt = f"""You are given a conversation with two or more people involved: {conversation}. And the context: {context}. 
    OUTPUT FORMAT. DO NOT SAY ANYTHING ELSE:
    {{"summary": "", "threaten": ""}} 
    For the 'summary' key, please summarize the conversation as well as the context. Keep it succinct. If there is no context then "summary": "".
    For the 'threaten' key, please indicate "yes" or "no" based on the conversation and the context. If the conversation is irrelavent, indicate "no".
    """

    kwargs = {
        "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        })
    }
    
    try:
        response = bedrock_client.invoke_model(**kwargs)
        response_body = response['body'].read() 
        result = json.loads(response_body) 
        print(result)
        output = json.loads(result['content'][0]['text']) 
        
    except Exception as e:

        print(f"Error occurred: {e}")
        context = f"""Context before: {context}. Context after: {conversation}"""
        return {"summary": f"{context}", "threaten": ""}  

    return output

if __name__ == "__main__":
    context = ""
    conversation = ""
    print(threaten_detection(context=context,conversation=conversation))