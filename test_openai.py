"""
Quick test to verify OpenAI API key works
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: OPENAI_API_KEY not found in environment!")
    exit(1)

print(f"API Key found: {api_key[:20]}...{api_key[-4:]}")

try:
    client = OpenAI(api_key=api_key)

    # Simple test call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'API key works!'"}],
        max_tokens=10
    )

    print(f"✓ Success! Response: {response.choices[0].message.content}")
    print("✓ OpenAI API key is valid and working!")

except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
