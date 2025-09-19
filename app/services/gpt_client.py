from groq import AsyncGroq
from app.core.config import settings

# Initialize the async Groq client once when the module is loaded
# It will automatically pick up the API key from the environment via our settings
try:
    async_groq_client = AsyncGroq(api_key=settings.GORQ_API_KEY)
    print("AsyncGroq client initialized successfully.")
except Exception as e:
    print(f"Failed to initialize AsyncGroq client: {e}")
    async_groq_client = None

async def generate_instruction(prompt: str) -> str:
    """
    Sends a prompt to the Groq API using the official Python SDK.
    """
    if not async_groq_client:
        return "Error: Groq client is not initialized. Please check your API key."

    try:
        # Use a non-streaming call, as our endpoint returns a single JSON object
        chat_completion = await async_groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert tutor for Data Structures and Algorithms, providing clear, personalized lessons."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gemma2-9b-it", # Or another model like "gemma2-9b-it"
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False, # We want the full response at once
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"An error occurred while communicating with Groq API: {e}")
        return "Error: Failed to generate instruction from the AI service."