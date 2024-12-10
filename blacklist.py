import sys
import pydnsbl

ip_checker = pydnsbl.DNSBLIpChecker()

result = ip_checker.check(sys.argv[1])
print(result.blacklisted, end='')