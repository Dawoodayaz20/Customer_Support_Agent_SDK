from agents import Agent, Runner, set_tracing_disabled, RunContextWrapper, AgentHooks, RunHooks, function_tool
from agents.extensions.models.litellm_model import LitellmModel
from dataclasses import dataclass
import os
from dataclasses import dataclass

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@dataclass
class Restaurant_info:
  name: str
  data: list[str]
  menu_data: dict

rest_data = Restaurant_info(
    name="Buns&Burger",
    data=[
    "Buns and Burger is an online restaurant.",
    "It does not have a physical location.",
    "Known for burgers and pizzas.",
    "Customers can order online and add items to a cart."
    ],
    menu_data={
      "Burgers":
     [
      { "name": "Zinger Cheeseburger", "id": 101, "price": "$5.99"},
      { "name": "Mega Zinger Burger", "id": 102, "price": "$4.99"},
      { "name": "Bacon Zinger Burger", "id": 103, "price": "$6.99"},
      { "name": "Libertine Burger", "id": 104, "price": "$7.99"},
      { "name": "3 Zingers Deal", "id": 105, "price": "$19.99"},
      { "name": "4 Zingers Deal", "id": 106, "price": "$24.99"}
    ],
      "Pizza": [
      { "name": "Cheese Pizza", "id": 201, "price": "$11.99"},
      {"name": "Chicken Fajita Pizza","id": 202,"price" : "$12.99"},
      {"name": "Chicken Supreme Pizza","id": 203,"price" : "$13.99"},
      {"name": "Chicken Tikka Pizza","id": 204,"price" : "$14.99"},
      {"name": "Chicken Malai Boti Pizza","id": 205,"price" : "$15.99"}
    ]
  })

@function_tool
async def get_restaurant_data(ctx: RunContextWrapper[Restaurant_info]):
  """ Function for getting restaurant data. """
  return f"Restaurant name is {rest_data.name} restaurant info is {rest_data.data}"

@function_tool
async def get_menu(ctx: RunContextWrapper[Restaurant_info]):
  """ Funcion for getting menu of Buns&Burger restaurant """
  return f"Menu data for restaurant is {rest_data.menu_data}"

async def kickoff(question: str):
  Restaurant_manager = Agent[Restaurant_info](
    name="Agent Manager",
    instructions="As the friendly and knowledgeable manager of 'Buns&Burger' online restaurant, your goal is to provide excellent customer service. Utilize the available tools to retrieve information about the restaurant and its menu. Respond to user inquiries in a helpful and polite manner, ensuring they have the information they need to order.",
    model=LitellmModel
    (
      model="gemini/gemini-1.5-flash", 
      api_key=GEMINI_API_KEY
    ),
    tools=[get_restaurant_data, get_menu]
  )

  result = await Runner.run(Restaurant_manager, question)
  return result.final_output