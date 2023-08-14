import requests

proxies = []

# Get proxies from raw text files
raw_proxy_sites = ['https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt', 'https://raw.githubusercontent.com/zloi-user/hideip.me/main/https.txt',' https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt',' https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt']
for site in raw_proxy_sites:
    response = requests.get(site)
    for line in response.text.split('\n'):
        if ':' in line:
            ip, port = line.split(':', maxsplit=2)[:2]
            proxies.append(f'{ip}:{port}')

with open('http.txt', 'w') as f:
    for proxy in proxies:
        f.write(proxy + '\n')
