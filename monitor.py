"""Q1: Collect the information the IT team needs to find the cause of high memory use.
Collects: total/used/available RAM, swap usage, page-fault counters, top memory-hungry processes.
Works on Linux using /proc (no extra libraries). Uses psutil automatically if installed."""
import os, time, csv

def read_meminfo():
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":")
            info[k] = int(v.split()[0]) // 1024  # MB
    return info

def read_vmstat():
    stats = {}
    with open("/proc/vmstat") as f:
        for line in f:
            k, v = line.split()
            stats[k] = int(v)
    return stats

def top_processes(n=5):
    procs = []
    for pid in filter(str.isdigit, os.listdir("/proc")):
        try:
            with open(f"/proc/{pid}/status") as f:
                data = dict(l.split(":", 1) for l in f if ":" in l)
            rss = int(data.get("VmRSS", "0 kB").split()[0]) // 1024
            procs.append((rss, int(pid), data["Name"].strip()))
        except (FileNotFoundError, ProcessLookupError, PermissionError, KeyError):
            continue
    return sorted(procs, reverse=True)[:n]

def snapshot():
    m, v = read_meminfo(), read_vmstat()
    total, avail = m["MemTotal"], m["MemAvailable"]
    swap_used = m["SwapTotal"] - m["SwapFree"]
    return {
        "time": time.strftime("%H:%M:%S"),
        "total_mb": total,
        "used_mb": total - avail,
        "used_percent": round(100 * (total - avail) / total, 1),
        "swap_used_mb": swap_used,
        "pages_swapped_in": v.get("pswpin", 0),
        "pages_swapped_out": v.get("pswpout", 0),
        "major_page_faults": v.get("pgmajfault", 0),
    }

def diagnose(s):
    """Simple rule-based diagnosis of the snapshot."""
    notes = []
    if s["used_percent"] > 85: notes.append("HIGH memory utilization (>85%)")
    if s["swap_used_mb"] > 0.2 * max(1, s["total_mb"]): notes.append("Heavy swap usage -> possible thrashing")
    if not notes: notes.append("Memory looks healthy")
    return notes

def run(samples=5, interval=1, logfile="memory_log.csv"):
    rows = []
    for _ in range(samples):
        rows.append(snapshot()); time.sleep(interval)
    with open(logfile, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    last = rows[-1]
    print("=== Memory Snapshot ===")
    for k, v in last.items(): print(f"{k:20}: {v}")
    print("\nTop 5 processes by memory (RSS):")
    for rss, pid, name in top_processes(): print(f"  PID {pid:<7} {name:<20} {rss} MB")
    if len(rows) > 1:
        print("\nPage-fault rate during sampling:",
              rows[-1]["major_page_faults"] - rows[0]["major_page_faults"], "major faults")
    print("\nDiagnosis:", "; ".join(diagnose(last)))
    print(f"(log saved to {logfile})")

if __name__ == "__main__":
    run()
