import asyncio

from app.src.realtime import LocalEventStream


class AppUtils:

     @staticmethod
     async def life_span(app):
          print('server is starting...')
          asyncio.create_task(LocalEventStream.consume_data())
          yield
          print('server is shutting down...')
