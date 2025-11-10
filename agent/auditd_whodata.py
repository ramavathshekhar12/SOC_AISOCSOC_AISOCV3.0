# Minimal auditd whodata-ish reader: tails /var/log/audit/audit.log and emits parsed lines for SYSCALL/EXECVE
import time, json, os, re

SYSCALL_RE = re.compile(r'type=SYSCALL .* msg=audit\((?P<ts>[^)]+)\): .* exe="(?P<exe>[^"]*)" .* uid=(?P<uid>\d+) .*')
EXECVE_RE  = re.compile(r'type=EXECVE .* a0="(?P<a0>[^"]*)"')

def tail(path):
    with open(path, "r", errors="ignore") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5); continue
            yield line.rstrip("\n")

def events(path="/var/log/audit/audit.log"):
    cur = {"syscall": None, "execve": []}
    for line in tail(path):
        m1 = SYSCALL_RE.search(line)
        if m1:
            if cur["syscall"]:
                yield cur
                cur = {"syscall": None, "execve": []}
            cur["syscall"] = m1.groupdict()
            continue
        m2 = EXECVE_RE.search(line)
        if m2:
            cur["execve"].append(m2.groupdict())
            continue

if __name__ == "__main__":
    for e in events():
        print(json.dumps(e))
