import subprocess
import sys
import concurrent.futures
import json

def install_pip(name):
    subprocess.call([sys.executable, '-m', 'pip', 'install', name])

def check_ip(ip):
    ip_checker = pydnsbl.DNSBLIpChecker()
    try:
        result = ip_checker.check(ip)
        return ip, result.blacklisted
    except:
        return ip, None

def main(ip_addresses):
    results = {}
    executor = concurrent.futures.ThreadPoolExecutor()
    try:
        future_to_ip = {executor.submit(check_ip, ip): ip for ip in ip_addresses}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip, blacklisted = future.result()
            results[ip] = blacklisted
    finally:
        executor.shutdown(wait=True)
    print(json.dumps(results, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    try:
        import pydnsbl
    except ImportError:
        install_pip('pydnsbl')
        import pydnsbl  # Re-import after install

    ip_list = sys.argv[1:]
    main(ip_list)
