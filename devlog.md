# Session 1

## Thoughts: 

This project is a bank simulation using threads and semaphores in Python. Three tellers serve 50 customers. Key shared resources: the safe (max 2 tellers), the manager (max 1 teller), and the door (max 2 customers entering at once). 

## Brief Plan

Build the teller and customer threads with matching semaphores. Start small with 3 customers before scaling to 50. 

## Plan for next session

Set up globals and semaphore structure - Write skeleton teller thread - Write skeleton customer thread.

# Session 2 

## Thoughts 

No new developments since initial entry.

## Plan

- Create bank.py 
- Define all global semaphores: door (2), safe (2), manager (1), line lock (1) 
- Define per-teller semaphore arrays for customer↔teller signaling 
- Write teller() function — just print statements, no sleeps yet 
- Write customer() function — just print statements, no sleeps yet 
- Launch 3 tellers + 3 customers (not 50), join all threads.

## Reflection
Got `bank.py` set up with the globals, semaphores, and both thread functions.
Tried it with `NUM_CUSTOMERS = 3`; the threads start and the printouts look reasonable.
The basic semaphore wiring seems to be working for this small test.

## Next session
Test with more customers. Scale to 50 and look for race conditions.

# Session 3

## Thoughts so far
I want to convince myself the current semaphore setup is solid before cranking the number of customers up. The main worry is a deadlock if a teller or customer ends up waiting on the wrong semaphore, so this session is mostly about running the small case a few times and watching the behavior.

## Plan this session
- Run `python3 bank.py` a few times in a row (about 3–5 runs), optionally piping the output to a file so it is easier to compare.
- Make sure each run finishes on its own and does not hang; if it stalls for more than ~5 seconds, treat that as a deadlock and investigate.
- Skim the logs to confirm the general pattern: tellers announce they are ready, customers enter only after the bank is open, then pick tellers and finish their transactions.
- Pay attention to the manager/safe sections and look for anything that suggests more than one teller with the manager or too many tellers in the safe at once.
- If something looks suspicious or inconsistent, add more logging or adjust the synchronization before moving on to larger tests.

## Reflection
Ran `python3 bank.py` several times with 3 customers. The order of events changed from run to run, but every run finished within a second or so and printed `Bank closed.` with no hangs.
In the logs, customers only started entering after all three tellers said they were ready, and each customer paired cleanly with exactly one teller.
Withdrawals always went through the manager (one teller at a time), and the safe never had more than two tellers inside at once based on the interleaving of the messages.
Overall the small test looks stable enough to justify trying larger customer counts next session.

## Next session
Bumping `NUM_CUSTOMERS` up toward 10, then 20, watching for any slowdowns or weird ordering in the logs.
If that still looks healthy, run with the full 50 customers and confirm it still finishes without hanging.
If problems show up at higher loads (for example, customers getting stuck waiting), add focused logging around the manager and safe sections to see where threads are blocking.