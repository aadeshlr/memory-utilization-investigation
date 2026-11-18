"""Q3: Recommend improvements and verify them by simulation (before/after comparison).
Simulates a workload where many apps run together, so memory is over-committed.
Shows that adding RAM (more frames) and using LRU reduce page faults / thrashing."""
import random
from page_replacement import fifo, lru

random.seed(1)
def workload(apps=6, pages_per_app=8, length=400):
    """Each app has a working set; the OS switches between apps frequently."""
    refs = []
    for _ in range(length):
        app = random.randrange(apps)
        refs.append(app * 100 + random.choice(range(pages_per_app)))
    return refs

def main():
    refs = workload()
    print("BEFORE (little RAM, FIFO):    faults =", fifo(refs, 16))
    print("AFTER 1 (switch to LRU):      faults =", lru(refs, 16))
    print("AFTER 2 (double the RAM, LRU):faults =", lru(refs, 32))
    print("AFTER 3 (RAM x3, LRU):        faults =", lru(refs, 48))
    print("\nRecommendations:")
    for r in ["Add more RAM / close unused applications",
              "Use LRU-approximating replacement (Clock) instead of FIFO",
              "Limit the number of apps running together (control degree of multiprogramming)",
              "Fix memory leaks / restart the heaviest processes found by monitor.py",
              "Tune swappiness and use faster swap storage (SSD)"]:
        print(" -", r)
    print("\nVerification: re-run monitor.py after changes; check lower used%, "
          "lower swap use and a lower major page-fault rate.")

if __name__ == "__main__":
    main()
