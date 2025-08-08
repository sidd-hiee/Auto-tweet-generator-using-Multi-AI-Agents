from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage  # ✅ Correct import
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# ✅ Include the required conversion flag
llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',
    temperature=0.2,
    convert_system_message_to_human=True
)

# ✅ Correct use of SystemMessage
generation_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a twitter influencer assistant tasked with writing excellent twitter posts. "
                "Generate the best twitter post possible for user's input. "
                "If user provides critique, respond with a revised version of your previous attempts. "
                "Respond with only improved tweet and nothing else. "
                "If you got good feedback, keep returning the most recent improved tweet and nothing else."
            )
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a viral twitter influencer grading a tweet. "
                "Generate critique and recommendations for user's tweet. "
                "Always provide detailed recommendations, including requests for length, virality, style, etc. "
                "Keep the response concise and focused on actionable feedback. "
                "Do not say anything else, just a critique. "
                "If the tweet is good and no improvement needed, just say 'good tweet' and nothing else."
            )
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# ✅ Define your chains using prompt + LLM
generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm
