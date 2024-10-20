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

    prompt = f"""You are given a part of the conversation with two or more people involved: {conversation}. And the context: {context}. 
    OUTPUT FORMAT. DO NOT SAY ANYTHING ELSE:
    {{"threaten": "", "threat_type":""}} 
    For the "threaten" key value, you can only return either "yes" or "no". "yes" means there is threat (sexual harrasment, threatenings, harmful/malicious intentions terrorist intention) in the conversation. "no" means there is no such threat.
    For the "threat_type" key value, you must return "none" if there is no threat. Return the kind of threat using one or two words if there is threat(s).
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
        return {"threat_type": "", "threaten": "no"}  
    return output
if __name__ == "__main__":
    context = "what is the matter"
    conversation = "what is the matter"
    print(threaten_detection(context=context,conversation=conversation))