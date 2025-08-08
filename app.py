import streamlit as st


from langchain_core.messages import HumanMessage
from Reflection_Agent import app  # ✅ From your existing backend
st.title("🤖 Twitter Influencer Agent")
st.write("Hello! This is a test to check if Streamlit is rendering.")
st.set_page_config(page_title="Tweet Generator Agent", layout="centered")

st.title("🤖 Twitter Influencer Agent")
st.markdown("Enter a topic and get a viral tweet with expert critique.")

# Input box
topic = st.text_input("Enter your tweet topic:", placeholder="e.g. How AI can be dangerous")

# Trigger
if st.button("Generate Tweet") and topic:
    st.info("Running agent... please wait ⏳")
    
    # Run the LangGraph agent
    response = app.invoke([HumanMessage(content=topic)])
    
    # Show the process (optional)
    st.markdown("### Agent Process:")
    for msg in response:
        role = "🧠 Agent" if hasattr(msg, "name") and msg.name else "🗣️ You"
        st.markdown(f"**{role}:** {msg.content}")

    # Show final tweet
    st.success("### ✅ Final Tweet:")
    st.markdown(f"**{response[-1].content}**")
