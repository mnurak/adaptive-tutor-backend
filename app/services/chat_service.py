from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

from app.models.user import User
from app.schemas.chat import ConversationRequest
from app.services.cognitive_analyzer import ml_cognitive_analyzer_service
from app.crud.crud_cognitive_profile import profile as crud_profile
from app.core.config import settings # <-- Import settings

# --- STABILITY FIX ---
# Explicitly pass the API key from our validated settings object.
# This prevents the library from failing to find the environment variable.
chat_llm = ChatGroq(
    groq_api_key=settings.GORQ_API_KEY,
    model="openai/gpt-oss-20b", # Use the new Gemma 2 model
    temperature=0.7
)

# This prompt template includes placeholders for the chat history and the final user input.
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert DSA tutor. Your responses are personalized based on the student's cognitive profile provided. Keep your answers concise and engaging."),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}"),
    ]
)

class ConversationalChainService:
    def __init__(
        self,
        db: AsyncSession,
        current_user: User,
    ):
        self.db = db
        self.current_user = current_user

    async def _update_cognitive_profile(self, user_input: str) -> dict:
        inferred_update, _ = ml_cognitive_analyzer_service.analyze_prompt(
            user_input, 
            current_profile=self.current_user.cognitive_profile
        )
        if inferred_update.model_dump(exclude_unset=True):
            current_profile_dict = self.current_user.cognitive_profile.__dict__
            update_data = inferred_update.model_dump(exclude_unset=True)
            current_profile_dict.update(update_data)
            await crud_profile.update(
                self.db,
                db_obj=self.current_user.cognitive_profile,
                obj_in=current_profile_dict
            )
        return {}

    def get_full_prompt(self, user_input: str) -> str:
        profile = self.current_user.cognitive_profile
        profile_context = (
            f"[Student Profile Context: Use a {profile.input_preference.value} and "
            f"{profile.complexity_tolerance.value}-complexity approach.]\n\n"
        )
        return profile_context + user_input

    async def generate_response(self, request: ConversationRequest) -> str:
        await self._update_cognitive_profile(request.prompt)
        memory = ConversationBufferWindowMemory(
            k=5, return_messages=True, memory_key="history"
        )
        for msg in request.conversation_history:
            if msg.role == "user":
                memory.chat_memory.add_user_message(msg.content)
            else:
                memory.chat_memory.add_ai_message(msg.content)

        conversational_chain = (
            RunnablePassthrough.assign(
                history=lambda x: memory.load_memory_variables(x)["history"]
            )
            | prompt_template
            | chat_llm
        )
        
        enriched_input = self.get_full_prompt(request.prompt)
        response = await conversational_chain.ainvoke({"input": enriched_input})
        return response.content