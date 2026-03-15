# Session 1:
## Thoughts: 

This project is a bank simulation using threads and semaphores in Python. Three tellers serve 50 customers. Key shared resources: the safe (max 2 tellers), the manager (max 1 teller), and the door (max 2 customers entering at once). 

## Brief Plan

Build the teller and customer threads with matching semaphores. Start small with 3 customers before scaling to 50. 

## Plan for next session

Set up globals and semaphore structure - Write skeleton teller thread - Write skeleton customer thread.

#Session 2 

## Thoughts No new developments since initial entry.

## Plan

- Create bank.py 
- Define all global semaphores: door (2), safe (2), manager (1), line lock (1) 
- Define per-teller semaphore arrays for customer↔teller signaling 
- Write teller() function — just print statements, no sleeps yet 
- Write customer() function — just print statements, no sleeps yet 
- Launch 3 tellers + 3 customers (not 50), join all threads.