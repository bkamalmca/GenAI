from phi.agent import Agent, RunResponse
from phi.utils.pprint import pprint_run_response
from phi.model.groq import Groq
from dotenv import load_dotenv
from phi.utils.pprint import pprint_run_response

load_dotenv()

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile")
)
# Run agent and return the response as a variable
response: RunResponse = agent.run("Tell me a 2 sentence horror story", stream=False)
# Print the response in markdown format
pprint_run_response(response, markdown=False)
print(response.content)
