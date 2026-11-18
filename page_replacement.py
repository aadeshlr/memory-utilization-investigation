"""Q2: Simulate page replacement algorithms (FIFO, LRU, Optimal) and compare page faults."""
from collections import deque

def fifo(pages, frames):
    mem, q, faults = set(), deque(), 0
    for p in pages:
        if p not in mem:
            faults += 1
            if len(mem) == frames: mem.remove(q.popleft())
            mem.add(p); q.append(p)
    return faults

def lru(pages, frames):
    mem, faults = [], 0          # list ordered: least recently used first
    for p in pages:
        if p in mem: mem.remove(p)
        else:
            faults += 1
            if len(mem) == frames: mem.pop(0)
        mem.append(p)
    return faults

def optimal(pages, frames):
    mem, faults = [], 0
    for i, p in enumerate(pages):
        if p in mem: continue
        faults += 1
        if len(mem) < frames: mem.append(p); continue
        # evict page used farthest in the future (or never)
        def next_use(x):
            return pages.index(x, i + 1) if x in pages[i + 1:] else float("inf")
        mem.remove(max(mem, key=next_use)); mem.append(p)
    return faults

ALGOS = {"FIFO": fifo, "LRU": lru, "Optimal": optimal}

def compare(pages, frame_sizes=(3, 4, 5)):
    print(f"Reference string: {pages}\n")
    print(f"{'Frames':<8}" + "".join(f"{a:<10}" for a in ALGOS))
    for f in frame_sizes:
        print(f"{f:<8}" + "".join(f"{fn(pages, f):<10}" for fn in ALGOS.values()))
    n = len(pages)
    print(f"\nTotal references: {n}")
    for f in frame_sizes:
        print(f"Hit ratio with {f} frames:", {a: round(1 - fn(pages, f) / n, 2) for a, fn in ALGOS.items()})

def belady_demo():
    s = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    print("\nBelady's anomaly demo (FIFO):", f"3 frames -> {fifo(s,3)} faults,", f"4 frames -> {fifo(s,4)} faults")

if __name__ == "__main__":
    compare([7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1])
    belady_demo()
