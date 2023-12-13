from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Loads the variables from .env into os.environ

client = OpenAI()

# Upload a file with an "assistants" purpose
file = client.files.create(
  file=open("Displacement_and_Gentrification_Recommendation_Inventory.csv", "rb"),
  purpose='assistants'
)

# Create an assistant with the csv file
assistant = client.beta.assistants.create(
    name="Data Analyst",
    instructions="You are an experienced data analyst studying Austin's Gentrification and Displacement Recommendation dataset. Provide insight and potential questions to explore.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
    file_ids=[file.id]
)

# Create a new thread
thread = client.beta.threads.create()

# Add message to thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="How many rows are in the dataset?"
)

# Start a run on the thread
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)

while run.status !="completed":
  run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
  )
  print(run.status)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(messages.data[0].content[0].text.value)
