import asyncio
import datetime
import os
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import requests


exector = ThreadPoolExecutor(max_workers=10)
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
addr = "https://fonts.googleapis.com/css2?family=Noto+Sans+SC&display=swap"
r = requests.get(addr, headers=headers)
rule = re.compile(r"https://[-\w\d/.]*")


def dl(uri, file_path):
    # await asyncio.sleep(0.1)
    print(uri, file_path, datetime.datetime.now())
    rr = requests.get(uri, headers=headers)
    with open(file_path, "wb") as wf:
        wf.write(rr.content)


async def main():
    loop = asyncio.get_event_loop()
    for l in r.text.splitlines():
        if re.search(rule, l):
            src = re.findall(rule, l)[0]
            split_path = urlparse(src)
            dirs = split_path.path.split("/")[1:-1]
            os.makedirs("/".join(dirs), exist_ok=True)

            file_path = "/".join(split_path.path.split("/")[1:])
            if not os.path.exists(file_path):
                await loop.run_in_executor(exector, dl, src, file_path)


asyncio.run(main())
