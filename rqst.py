import aiohttp
import asyncio
import json as jsn

class resp:
    def __init__(self, content, code):
        try:
            self.text = content.decode('utf-8')
        except:
            self.text = ""
        self.json = lambda: jsn.loads(content.decode('utf-8'))
        self.content = content
        self.status_code = code

async def get(url, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            content = await response.read()
            code = response.status
            
            return resp(content, code)

async def post(url, headers=None, json=None, data=None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json, data=data) as response:
            content = await response.read()
            code = response.status
            
            return resp(content, code)