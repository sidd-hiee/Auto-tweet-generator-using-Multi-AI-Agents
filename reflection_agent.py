from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, MessageGraph
from chains import generation_chain, reflection_chain
from langchain_core.messages import HumanMessage, BaseMessage

# Load environment variables (e.g., your API key)
load_dotenv()

# Create a LangGraph message graph
graph = MessageGraph()

# Define node labels
REFLECT = "reflect"
GENERATE = "generate"

# Generation node: generates a tweet
def generate_node(state: List[BaseMessage]):
    result = generation_chain.invoke({"messages": state})
    return state + [result]

# Reflection node: critiques the tweet and gives feedback
def generate_reflection_node(state: List[BaseMessage]):
    result = reflection_chain.invoke({"messages": state})
    return state + [HumanMessage(content=result.content)]

# Add nodes to the graph
graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, generate_reflection_node)

# Set starting point
graph.set_entry_point(GENERATE)

# Define stopping logic
def should_continue(state: List[BaseMessage]):
    if len(state) > 4:
        return END
    return REFLECT

# Define conditional and regular edges
graph.add_conditional_edges(GENERATE, should_continue, {
    REFLECT: REFLECT,
    END: END
})

graph.add_edge(REFLECT, GENERATE)

# Compile the graph into an app
app = graph.compile()

# Invoke the app with an initial human message
response = app.invoke(
    HumanMessage(content="")
)

# Print the final result
print("\n🧠 Final Tweet or Feedback:")
print(response[-1].content)
