import requests
import concurrent.futures
import os
from time import sleep, perf_counter
vao = input("nhập tên file cần lọc.   ")
ra = input("nhập output ")
target_url = "http://httpbin.org/ip"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def thanh():
    print("\033[1;37m——————————————————————————")

clear()
thanh()

proxy_list = open(vao).read().split('\n')
output_file = ra

# Kiểm tra và xóa file có tên trùng (nếu tồn tại)
if os.path.exists(output_file):
    os.remove(output_file)

clear()
print(" \033[1;32mVui lòng chờ vài giây...")
sleep(3)
print(" \033[1;37mBắt đầu chạy tool. Vui lòng không nhấn gì hết!")
sleep(2)

def test_proxy(proxy):
    try:
        response = requests.get(target_url, proxies={"http": proxy, "https": proxy}, timeout=20)
        if response.status_code in [200, 202, 504, 503, 502, 500]:
            print ('\033[1;37m[\033[1;32m+\033[1;37m] \033[1;37m[ \033[1;32mLive\033[1;37m ] > \033[1;32m'+proxy)
            with open(output_file,'a') as file:
                file.write(proxy+'\n')
        elif response.status_code == 403:
            pass
        elif response.status_code == 409:
            pass
        else:
            print(f"\033[1;37m[ \033[1;33mHop \033[1;37m] \033[1;33m{response.status_code} \033[1;37m> \033[1;33m"+proxy)
    except requests.exceptions.RequestException as e:
        print(f'\033[1;37m[ \033[1;31mBad \033[1;37m] > \033[1;31m'+proxy)

def main():
    start_time = perf_counter()
    count = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10000) as executor:
        futures = [executor.submit(test_proxy, proxy) for proxy in proxy_list]
        
        for future in concurrent.futures.as_completed(futures):
            count += 1

    end_time = perf_counter()
    
    print(f"\033[1;37mĐã lọc proxy hoàn tất. Hiện tại trong danh sách \033[1;32m{output_file} \033[1;37mđang có \033[1;32m%s \033[1;37mproxies-live" % (len(open(output_file).readlines())))
    print(f"Thời gian kiểm tra: {end_time - start_time:.2f} giây")
    print(f"Số lượng proxy đã kiểm tra: {count}")

if __name__ == "__main__":
    main()
