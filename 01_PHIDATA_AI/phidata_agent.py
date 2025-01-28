from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile")
)

#agent.print_response("Write a poem in 4 lines about a AI and human")
#agent.print_response("Can AI control human in future?")

while True:
    user_input = input("You: ")
    if user_input == "bye":
        break
    agent.print_response(user_input)