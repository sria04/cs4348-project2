# Session 1:
## Thoughts: 

This project is a bank simulation using threads and semaphores in Python. Three tellers serve 50 customers. Key shared resources: the safe (max 2 tellers), the manager (max 1 teller), and the door (max 2 customers entering at once). 

## Brief Plan

Build the teller and customer threads with matching semaphores. Start small with 3 customers before scaling to 50. 

## Plan for next session

Set up globals and semaphore structure - Write skeleton teller thread - Write skeleton customer thread.