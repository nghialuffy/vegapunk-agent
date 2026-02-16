"""
LangGraph workflow definition for the Research & Teaching Agent.

This creates a deterministic, linear pipeline:
  setup → research → synthesis → writing → publish
"""

from langgraph.graph import StateGraph, END
from src.models import AgentState
from src.nodes import (
    setup_node,
    research_node,
    synthesis_node,
    writing_node,
    publish_node
)


def create_agent_graph():
    """
    Create and compile the LangGraph workflow.

    Returns:
        Compiled StateGraph ready for execution
    """
    # Create workflow with AgentState schema
    workflow = StateGraph(AgentState)

    # Add all nodes
    workflow.add_node("setup", setup_node)
    workflow.add_node("research", research_node)
    workflow.add_node("synthesis", synthesis_node)
    workflow.add_node("writing", writing_node)
    workflow.add_node("publish", publish_node)

    # Define linear flow
    workflow.set_entry_point("setup")
    workflow.add_edge("setup", "research")
    workflow.add_edge("research", "synthesis")
    workflow.add_edge("synthesis", "writing")
    workflow.add_edge("writing", "publish")
    workflow.add_edge("publish", END)

    # Compile the graph
    return workflow.compile()


def run_agent(topic: str, target_audience: str = "intermediate developers", repo_dir: str = None) -> AgentState:
    """
    Run the complete agent pipeline.

    Args:
        topic: The topic to create a course about
        target_audience: Description of the target audience
        repo_dir: Optional directory containing existing repositories to use

    Returns:
        Final agent state with all generated content
    """
    # Initialize state
    initial_state: AgentState = {
        "topic": topic,
        "target_audience": target_audience,
        "repo_dir": repo_dir,
        "repo_info": {},
        "research_sources": [],
        "raw_notes": "",
        "knowledge_base": "",
        "lesson_outline": [],
        "lessons": {},
        "github_repo_url": ""
    }

    # Create and run graph
    graph = create_agent_graph()
    final_state = graph.invoke(initial_state)

    return final_state
