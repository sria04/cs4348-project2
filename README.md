# Bank simulation (threads & semaphores)

A small Python simulation of a bank with 3 tellers and 50 customers. Customers and tellers run in separate threads; semaphores limit how many people can use the door, the manager’s office, and the safe at once.

## How to run

```bash
python3 bank.py
```

You should see tellers announce they’re ready, then customers entering, getting served (deposits or withdrawals), and leaving. At the end you get “Bank closed.” Every run finishes on its own; if it hangs, that would indicate a deadlock (hasn’t happened in testing).

## What’s going on

- **Door:** at most 2 customers can be stepping through at once.
- **Manager:** only 1 teller can be with the manager at a time (needed for withdrawals).
- **Safe:** at most 2 tellers can be in the safe at once.

Customers pick a random transaction (deposit or withdrawal), wait until the bank is open (all tellers ready), then grab a free teller. Tellers and customers coordinate with per-teller semaphores so each customer is served by one teller from start to finish.

## Files

- `bank.py` — main simulation (config at the top: `NUM_TELLERS`, `NUM_CUSTOMERS`).
- `devlog.md` — session notes and what I did each time.
- `run_10.txt`, `run_20.txt`, `run_50.txt` — sample outputs from runs with 10, 20, and 50 customers.
