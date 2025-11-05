import asyncio

from google.adk.runners import InMemoryRunner

from .agent import get_root_agent
from .coa_plugin import CoaPlugin

async def main():
  runner = InMemoryRunner(
      agent=get_root_agent(),
      app_name='financial_coordinator',
      plugins=[CoaPlugin()],
  )

  session = await runner.session_service.create_session(
      user_id='user',
      app_name='test_app_with_plugin',
  )

if __name__ == "__main__":
  asyncio.run(main())
