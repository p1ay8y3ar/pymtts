import asyncio

from pymtts import async_Mtts


async def test():
    mtts = async_Mtts()
    models = await mtts.get_lang_models()
    for model in models:
        print(dict(model))


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
