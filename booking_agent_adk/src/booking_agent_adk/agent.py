"""Booking agent and sub-agents, handling the confirmation and payment of bookable events."""

import json
import random
from typing import Any


from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.tool_context import ToolContext
from booking_agent_adk.task_manager import AgentWithTaskManager
import booking_agent_adk.prompt as prompt
from booking_agent_adk.tools.memory import memorize
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool


class BookingAgent(AgentWithTaskManager):
    """An agent that handles booking requests."""

    create_reservation = Agent(
        model="gemini-2.0-flash-001",
        name="create_reservation",
        description="Create a reservation for the selected item.",
        instruction=prompt.CONFIRM_RESERVATION_INSTR,
    )

    payment_choice = Agent(
        model="gemini-2.0-flash-001",
        name="payment_choice",
        description="Show the users available payment choices.",
        instruction=prompt.PAYMENT_CHOICE_INSTR,
    )

    process_payment = Agent(
        model="gemini-2.0-flash-001",
        name="process_payment",
        description="Given a selected payment choice, processes the payment, completing the transaction.",
        instruction=prompt.PROCESS_PAYMENT_INSTR,
    )

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']

    def __init__(self):
        self._agent = self._build_agent()
        self._user_id = 'remote_agent'
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    def get_processing_message(self) -> str:
        return 'Processing the booking request...'

    def _build_agent(self) -> LlmAgent:
        """Builds the LLM agent for the booking agent."""
        return LlmAgent(
            model='gemini-2.0-flash-001',
            name='booking_agent',
            description=(
                'This agent handles the booking process for the user for the given itinerary.'
            ),
            instruction=prompt.BOOKING_AGENT_INSTR,
            tools=[
                memorize,
                AgentTool(agent=self.create_reservation),
                AgentTool(agent=self.payment_choice),
                AgentTool(agent=self.process_payment),
            ]            
        )
