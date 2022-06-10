class MttsLangModel:
    Name = None
    DisplayName = None
    LocalName = None
    ShortName = None
    Gender = None
    Locale = None
    LocaleName = None
    StyleList = []
    SampleRateHertz = None
    VoiceType = None
    Status = None
    RolePlayList = []

    def __init__(self, arg: dict):
        for key, value in arg.items():
            setattr(MttsLangModel, key, value)

    def keys(self):
        return (
            "Name", "DisplayName", "LocalName", "ShortName", "Gender",
            "Locale", "LocaleName", "StyleList", "SampleRateHertz", "VoiceType",
            "Status", "RolePlayList")

    def __getitem__(self, item):
        return getattr(self, item)


class MttsException(Exception):
    pass

from datetime import datetime
import uuid


def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")


def get_connect_id():
    return str(uuid.uuid4()).replace("-", "").upper()


TOKEN_URL: str = "https://azure.microsoft.com/en-gb/services/cognitive-services/text-to-speech/"
LANG_MODEL_URL: str = "https://eastus.tts.speech.microsoft.com/cognitiveservices/voices/list"
WSS_CONNECT_URL: str = "wss://eastus.tts.speech.microsoft.com/cognitiveservices/websocket/v1?Authorization=bearer%20{}&X-ConnectionId={}"
FIRST_JSON: str = '''Path: speech.config\r\nX-RequestId: {}\r\nX-Timestamp: {}\r\nContent-Type: application/json\r\n\r\n{{"context": {{"system": {{"name": "SpeechSDK","version": "{}","build": "JavaScript","lang": "JavaScript"}},"os": {{"platform": "Browser/MacIntel","name": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36","version": "5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"}}}}}}'''

SECOND_JSON: str = '''Path: synthesis.context\r\nX-RequestId: {}\r\nX-Timestamp: {}\r\nContent-Type: application/json\r\n\r\n{{"synthesis": {{"audio": {{"metadataOptions": {{"bookmarkEnabled": false,"sentenceBoundaryEnabled": false,"visemeEnabled": false,"wordBoundaryEnabled": false}},"outputFormat": "audio-{}khz-160kbitrate-mono-mp3"}},"language": {{"autoDetection": false}}}}}}'''

THIRD_SSML: str = """Path: ssml\r\nX-RequestId: {}\r\nX-Timestamp: {}\r\nContent-Type: application/ssml+xml\r\n\r\n<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="{}"><mstts:express-as style="{}"><prosody rate="{}%" pitch="{}%">{}</prosody></mstts:express-as></voice></speak>"""
