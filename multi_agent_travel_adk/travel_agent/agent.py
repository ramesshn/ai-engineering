"""Demonstration of Travel AI Conceirge using Agent Development Kit"""

from google.adk.agents import Agent

import travel_agent.prompt as prompt
from travel_agent.tools.memory import _load_precreated_itinerary
from travel_agent.sub_agents.inspiration.agent import inspiration_agent
from travel_agent.sub_agents.planning.agent import planning_agent
from travel_agent.sub_agents.booking.agent import booking_agent

root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="root_agent",
    description="A Travel Conceirge using the services of multiple sub-agents",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        inspiration_agent,
        planning_agent,
        booking_agent,
            ],
    before_agent_callback=_load_precreated_itinerary,
)