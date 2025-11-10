# Windows Event Log reader for Security and Sysmon channels
# Requires: pip install pywin32 (on Windows)
import time, json, platform, sys
if platform.system() != "Windows":
    print("Windows Event Reader must run on Windows.", file=sys.stderr); sys.exit(1)
import win32evtlog  # type: ignore

def read_channel(server='localhost', logtype='Security', seek_latest=True):
    h = win32evtlog.OpenEventLog(server, logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ if seek_latest else win32evtlog.EVENTLOG_SEQUENTIAL_READ
    while True:
        events = win32evtlog.ReadEventLog(h, flags, 0)
        if events:
            for e in events[::-1]: # chronological
                yield {
                    "TimeGenerated": str(e.TimeGenerated),
                    "EventID": e.EventID & 0xFFFF,
                    "SourceName": e.SourceName,
                    "EventCategory": e.EventCategory,
                    "EventType": e.EventType,
                    "RecordNumber": e.RecordNumber,
                    "ComputerName": e.ComputerName,
                    "Strings": e.StringInserts
                }
        time.sleep(1)

if __name__ == "__main__":
    for ev in read_channel(logtype="Security"):
        print(json.dumps(ev))
