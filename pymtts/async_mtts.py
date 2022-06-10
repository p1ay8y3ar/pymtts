
from .tools import MttsLangModel
from aiohttp import ClientSession
from .tools import get_connect_id, TOKEN_URL, LANG_MODEL_URL, FIRST_JSON, SECOND_JSON, THIRD_SSML, WSS_CONNECT_URL
from .tools import get_time
import re
from .tools import MttsException
import json
from typing import List
import websockets as ws
from websockets import ConnectionClosed
import asyncio


class Mtts:
    connection_id: str = get_connect_id()
    token: str = None
    _token_url: str = TOKEN_URL
    _lang_model_url: str = LANG_MODEL_URL
    lang_models: List[MttsLangModel] = []
    SpeechSDK_VERSION: str = "1.19.0"

    async def get_token(self) -> None:
        async with ClientSession() as session:
            async with session.get(self._token_url) as response:
                response = await response.read()
                to = re.compile(r"token: \"(.*?)\"")
                token = to.search(response.decode("utf-8")).group()
                if token is None:
                    raise MttsException("not found token")
                self.token = token.split("token: ")[1].replace('"', '')

    def token_check(func):
        async def wrapper(self, *args, **kwargs):
            if self.token is None:
                await self.get_token()
            return await func(self, *args, **kwargs)

        return wrapper

    def model_check(func):
        async def wrapper(self, *args, **kwargs):
            if len(self.lang_models) == 0:
                await self.get_lang_models()
            return await func(self, *args, **kwargs)

        return wrapper

    @token_check
    async def get_lang_models(self) -> list:
        '''
         get all support voice models
        :return: list
        '''
        headers = {"authorization": 'Bearer {}'.format(self.token)}
        async with ClientSession(headers=headers) as session:
            async with session.get(self._lang_model_url) as response:
                response = await response.read()
                data = json.loads(response)
                self.lang_models.extend([MttsLangModel(m) for m in data])
        return self.lang_models

    @token_check
    async def mtts(self, text: str, short_name: str, style: str = "general", rate: int = 0, pitch: int = 0,
                   kmhz: int = 24) -> bytes:
        '''
        :param text: text to convert
        :param short_name:The name of the language pack to use
        :param style:The language style to use, defaults to 'general'
        :param rate:Speech rate, default 0
        :param pitch: intonation, default 0
        :param kmhz:
        :return: bytes,buffer of audio
        '''
        async with ws.connect(WSS_CONNECT_URL.format(self.token, self.connection_id)) as websocket:

            await websocket.send(FIRST_JSON.format(self.connection_id, get_time, self.SpeechSDK_VERSION))
            await websocket.send(SECOND_JSON.format(self.connection_id, get_time(), kmhz))
            await websocket.send(
                THIRD_SSML.format(self.connection_id, get_time(), short_name, style, rate, pitch, text))
            await websocket.recv()
            await websocket.recv()
            await websocket.recv()
            final_date = b''
            while True:
                try:
                    data = await websocket.recv()
                    if type(data) is bytes:
                        if b'Path:audio' in data:
                            final_date += data[data.index(b"Path:audio") + 12:]
                    elif "Path:turn.end" in data:
                        return final_date
                except ConnectionClosed as e:
                    if e.code == 1006:
                        await asyncio.sleep(2)
                        break
