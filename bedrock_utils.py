import boto3
import json
import streamlit as st

def get_bedrock_credentials():
    secrets_client = boto3.client('secretsmanager')
    secret_name = "bedrocksecrets"
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        secrets = json.loads(response['SecretString'])
        return {
            'region_name': secrets.get('AWS_REGION'),
            'aws_access_key_id': secrets.get('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': secrets.get('AWS_SECRET_ACCESS_KEY'),
            'kendra_index_id': secrets.get('AWS_KENDRA_INDEX_ID'),
            'session_secret': secrets.get('SESSION_SECRET'),
            'session_secret_bdm1': secrets.get('SESSION_SECRET_BDM1'),
            'session_secret_bmd2': secrets.get('SESSION_SECRET_BMD2'),
            'session_secret_instructor1': secrets.get('SESSION_SECRET_INSTRUCTOR1'),
            'session_secret_instructor2': secrets.get('SESSION_SECRET_INSTRUCTOR2')
        }
    except Exception as e:
        st.error(f"Error retrieving Bedrock credentials: {e}")
        return None

def list_available_models():
    claude_models = [
        ("anthropic.claude-3-haiku-20240307-v1:0", "Claude 3 Haiku 1.0"),
        ("anthropic.claude-v2", "Claude 2.0"),
        ("anthropic.claude-v2:1", "Claude 2.1"),
        ("anthropic.claude-3-sonnet-20240229-v1:0", "Claude 3 Sonnet 1.0"),
        ("anthropic.claude-3-5-sonnet-20240620-v1:0", "Claude 3.5 Sonnet 1.0"),
        ("anthropic.claude-instant-v1", "Claude Instant 1.x")
    ]
    return claude_models

def invoke_bedrock_model(prompt, access_key, secret_key, model_id):
    try:
        bedrock_client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='us-east-1'
        )

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        })

        response = bedrock_client.invoke_model_with_response_stream(
            modelId=model_id,
            body=body,
        )

        stream = response.get("body")
        parsed_response = ""

        for event in stream:
            chunk = event.get('chunk')
            if chunk:
                message = json.loads(chunk.get("bytes").decode())
                if "content_block_delta" in message.get('type', ''):
                    parsed_response += message['delta'].get("text", "")
                elif "message_stop" in message.get('type', ''):
                    break

        return parsed_response
    except Exception as e:
        st.error(f"Error in invoking model: {e}")
        return "Response not available due to API error."

def summarize_markdown(markdown_content):
    if markdown_content.strip():
        summarized_content = markdown_content[:500] + "..."
        return summarized_content
    else:
        return "No insights available from the provided learning resources." 