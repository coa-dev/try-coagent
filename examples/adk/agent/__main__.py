import asyncio
import aioconsole

from coa_dev_coagent import CoagentClient
from datetime import datetime
from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part

from .agent import get_root_agent
from .coa_plugin import CoaPlugin
from .json import pretty_print_json

APP_NAME = 'financial_coordinator'
USER_ID = 'coa_user'

async def main():
    coa = CoagentClient()
    prompt_number = 1
    turn_number = 1

    runner = InMemoryRunner(
        agent=get_root_agent(),
        app_name=APP_NAME,
        plugins=[CoaPlugin(coa=coa)],
    )

    print("Starting interactive session with the Financial Coordinator agent.")

    session = await runner.session_service.create_session(
        user_id=USER_ID,
        app_name=APP_NAME,
    )

    print(f"Session created: {session.id}")

    while True:
        user_query = await aioconsole.ainput('[user]: ')

        if prompt_number == 1 and turn_number == 1:
            coa.log_session_start(
                session_id=session.id,
                prompt=user_query,
                prompt_number=prompt_number,
                turn_number=turn_number,
            )
            prompt_number += 1
            turn_number += 1

        run_id = f'adk-run-{datetime.now().astimezone().isoformat()}'
        coa.log_run_start(
            run_id=run_id,
            prompt=user_query,
        )

        print(f"[debug] User query received: {user_query}")

        if user_query.lower() in ['exit', 'quit']:
            print("Exiting the conversation.")
            break

        new_message = Content(role='user', parts=[Part(text=user_query)])

        print(f"[debug] Created new message: {new_message}")

        events = runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=new_message,
        )

        print("[debug] Processing events...")

        final_response = ""
        i = 0

        async for event in events:
            print(f"[event {i}]: {event}")

            i += 1
            if hasattr(event, 'author') and event.author == 'financial_coordinator':
                if event.is_final_response():
                    final_response = event.content.parts[0].text
                    pretty = pretty_print_json(final_response, title="Final Response Event")
                    print(pretty)

if __name__ == "__main__":
  asyncio.run(main())
