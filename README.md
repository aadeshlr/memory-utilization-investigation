# Investigating High Memory Utilization (OS Assignment)

**Scenario:** A software company's computers slow down when many applications run together. Physical memory is almost full and the OS keeps moving pages between RAM and secondary storage (swap), which suggests inefficient allocation or excessive demand from some applications.

## Project files
| File | Answers | What it does |
|---|---|---|
| `monitor.py` | Q1 | Collects RAM usage, swap usage, page-fault counters and top memory-hungry processes, then diagnoses |
| `page_replacement.py` | Q2 | Simulates FIFO, LRU and Optimal page replacement and compares page faults / hit ratio; demos Belady's anomaly |
| `recommendations.py` | Q3 | Simulates before/after improvements to verify they reduce page faults |
| `main.py` | All | Runs everything |

## How to run
Requires Python 3 (Linux, no extra libraries).
```
python3 main.py
```

## Q1 – What information should the IT team collect?
- Total, used and available RAM (utilization %)
- Swap used, pages swapped in/out (`pswpin`, `pswpout`)
- Major page-fault rate (`pgmajfault`) - a high rate means thrashing
- Per-process memory (RSS) to find the heaviest applications / memory leaks
- Number of apps running concurrently and CPU wait time

## Q2 – How to evaluate memory management and page replacement?
Run the same page reference string through FIFO, LRU and Optimal for different frame counts and compare page faults and hit ratio. Optimal is the lower bound (not implementable in practice), LRU is close to it, FIFO is simplest but worst and can show Belady's anomaly. Paging vs. segmentation and allocation policies (first/best fit) are evaluated by fragmentation and fault counts.

## Q3 – Recommendations and verification
1. Add RAM or close unnecessary applications
2. Use LRU/Clock replacement instead of FIFO
3. Limit the degree of multiprogramming to prevent thrashing
4. Fix memory leaks / restart heavy processes
5. Tune swappiness; use SSD for swap

**Verification:** `recommendations.py` shows page faults dropping after each change; on a real system re-run `monitor.py` and confirm lower memory %, lower swap use and lower page-fault rate.
