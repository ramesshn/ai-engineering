from common.server import A2AServer
from common.types import AgentCard, AgentCapabilities, AgentSkill, MissingAPIKeyError
from booking_agent_adk.task_manager import AgentTaskManager
from booking_agent_adk.agent import BookingAgent
import click
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

@click.command()
@click.option("--host", default="localhost")
@click.option("--port", default=10002)
def main(host, port):
    try:
        # Check for API key only if Vertex AI is not configured
        if not os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "TRUE":
            if not os.getenv("GOOGLE_API_KEY"):
                raise MissingAPIKeyError(
                    "GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE."
                )
        
        capabilities = AgentCapabilities(streaming=False)
        skill = AgentSkill(
            id="process_booking",
            name="Process Booking Tool",
            description="Helps with the booking process for users to book a flight and hotel reservation given the itinerary.",
            tags=["booking"],
            examples=["Can you book me flight for the given itinerary?"],
        )
        agent_card = AgentCard(
            name="Booking Agent",
            description="This agent handles the booking process for the customer for the  given itinerary.",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )
        server = A2AServer(
            agent_card=agent_card,
            task_manager=AgentTaskManager(agent=BookingAgent()),
            host=host,
            port=port,
        )
        server.start()
    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)
    
if __name__ == "__main__":
    main()