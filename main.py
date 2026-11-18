"""Run the whole investigation: python main.py"""
import monitor, page_replacement, recommendations
print("\n########## PART 1: DATA COLLECTION ##########");  monitor.run(samples=3, interval=1)
print("\n########## PART 2: PAGE REPLACEMENT ##########"); page_replacement.compare([7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]); page_replacement.belady_demo()
print("\n########## PART 3: RECOMMENDATIONS ##########");   recommendations.main()
