from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    llm = ChatOpenAI(
        model="gpt-4.1-mini",
    )
    task = "Recommend an Album for me from 'https://www.discogs.com/sell/list?format=CD&ships_from=United+Kingdom&style=Pop+Rock&format_desc=Album&year=2016'"
    agent = Agent(
        task=task, 
        llm=llm,
        save_conversation_path="./conversation_history.json",
        )
    history = await agent.run()
    
    
    history.structured_output

if __name__ == "__main__":
    asyncio.run(main())
