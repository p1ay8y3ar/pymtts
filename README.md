# pymtts

A python package for using Azure smart AI speech

## how to install 
```shell
pip3 install --upgrade pymtts
```
## sample use case

```python
from pymtts import async_Mtts
mtts = async_Mtts()
mp3_bytes_buffer = await mtts.mtts("欢迎使用pymtts","zh-CN-YunxiNeural", 'general', 0, 0, )
```
## get all supported voice models

```python
from pymtts import async_Mtts
mtts = async_Mtts()
models= await mtts.get_lang_models()
```