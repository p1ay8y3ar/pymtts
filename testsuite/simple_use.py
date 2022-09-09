import asyncio

from pymtts import async_Mtts


async def test():
    mtts = async_Mtts()
    mp3_bytes_buffer = await mtts.mtts("欢迎使用pymtts", "zh-CN-YunxiNeural", 'general', 0, 0, )
    print(mp3_bytes_buffer)
    with open("aaaa.mp3", "wb") as f:
        f.write(mp3_bytes_buffer)


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
