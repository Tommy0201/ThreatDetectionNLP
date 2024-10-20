import boto3
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def summary(conversation):
    bedrock_client = boto3.client('bedrock-runtime', 
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN')
    )

    prompt = f"""Summarize this conversation in the most succint way while keeping all the key information: {conversation}. 
    OUTPUT FORMAT. DO NOT SAY ANYTHING ELSE:
    {{"summary": ""}} 
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
    

    response = bedrock_client.invoke_model(**kwargs)
    response_body = response['body'].read() 
    result = json.loads(response_body) 
    output = json.loads(result['content'][0]['text']) 
    return output

# if __name__ == "__main__":
    conversation = "What is the matter"
    print(summary(conversation=conversation))