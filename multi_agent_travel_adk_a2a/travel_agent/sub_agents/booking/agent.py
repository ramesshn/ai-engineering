from travel_agent.sub_agents.booking.host_agent import HostAgent


booking_agent = HostAgent(['http://localhost:10002']).create_agent()