import threading
import random
import time

# Basic settings for the simulation
NUM_TELLERS = 3
NUM_CUSTOMERS = 3

# Limits for different shared parts of the bank
door_sem = threading.Semaphore(2)     # at most 2 customers entering at once
safe_sem = threading.Semaphore(2)     # at most 2 tellers in the safe
manager_sem = threading.Semaphore(1)  # only one teller can see the manager

# Customers should only enter once all tellers are ready
bank_open = threading.Semaphore(0)
tellers_ready = 0
tellers_ready_lock = threading.Lock()

# Simple queue where free tellers announce themselves
ready_tellers = []              # holds teller ids that are currently free
line_lock = threading.Semaphore(1)

# Per‑teller semaphores used as one‑bit signals
teller_sem = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
customer_sem = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
transaction_sem = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
done_sem = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
leave_sem = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]

# Shared slots per teller
teller_transaction = [None] * NUM_TELLERS   # "deposit" or "withdrawal"
teller_customer_id = [None] * NUM_TELLERS   # which customer this teller is serving

# How many customers have finished, total
customers_served = 0
customers_served_lock = threading.Lock()

# Keep output from different threads from getting jumbled
print_lock = threading.Lock()


def log(actor, actor_id, partner, partner_id, msg):
    """Print a line in a consistent format while holding a lock."""
    with print_lock:
        print(f"{actor} {actor_id} [{partner} {partner_id}]: {msg}")


# Teller thread
def teller(tid):
    global tellers_ready, customers_served

    # First time a teller runs, it marks itself as ready.
    with tellers_ready_lock:
        tellers_ready += 1
        if tellers_ready == NUM_TELLERS:
            # Last teller to arrive lets all customers know the bank is open.
            for _ in range(NUM_CUSTOMERS):
                bank_open.release()
    log("Teller", tid, "Teller", tid, "ready to serve customers")

    while True:
        # If everyone has already been helped, this teller can close.
        with customers_served_lock:
            if customers_served >= NUM_CUSTOMERS:
                break

        # Mark this teller as free so a customer can pick it.
        line_lock.acquire()
        ready_tellers.append(tid)
        line_lock.release()

        # Wait until some customer chooses this teller.
        teller_sem[tid].acquire()

        # We might have been woken up just so we can exit.
        with customers_served_lock:
            if customers_served >= NUM_CUSTOMERS:
                break

        cid = teller_customer_id[tid]

        log("Teller", tid, "Customer", cid, "asks what they want to do")
        # Let the customer know it's time to tell us the transaction.
        customer_sem[tid].release()

        # Wait until the customer sets the transaction type.
        transaction_sem[tid].acquire()
        txn = teller_transaction[tid]
        log("Teller", tid, "Customer", cid, f"got a {txn} request")

        # For withdrawals we have to see the manager first.
        if txn == "withdrawal":
            log("Teller", tid, "Customer", cid, "heading to the manager")
            manager_sem.acquire()
            log("Teller", tid, "Customer", cid, "talking to the manager")
            time.sleep(random.uniform(0.005, 0.03))
            log("Teller", tid, "Customer", cid, "done with the manager")
            manager_sem.release()

        # All transactions end up going through the safe.
        log("Teller", tid, "Customer", cid, "heading to the safe")
        safe_sem.acquire()
        log("Teller", tid, "Customer", cid, "inside the safe")
        time.sleep(random.uniform(0.01, 0.05))
        log("Teller", tid, "Customer", cid, "leaving the safe")
        safe_sem.release()

        # Let the customer know everything is finished.
        log("Teller", tid, "Customer", cid, "finished the transaction")
        done_sem[tid].release()

        # Wait until the customer has actually left our window.
        leave_sem[tid].acquire()
        log("Teller", tid, "Customer", cid, "customer left the window")

        with customers_served_lock:
            customers_served += 1

    log("Teller", tid, "Teller", tid, "closing")

# Customer thread
def customer(cid):
    # Pick a random transaction type for this customer.
    txn = random.choice(["deposit", "withdrawal"])
    log("Customer", cid, "Customer", cid, f"wants to make a {txn}")

    # Wait a bit, then try to walk into the bank.
    time.sleep(random.uniform(0, 0.1))
    door_sem.acquire()
    bank_open.acquire()   # make sure tellers are ready
    log("Customer", cid, "Customer", cid, "enters bank")
    door_sem.release()

    # Look for any teller that has marked itself as free.
    my_teller = None
    while my_teller is None:
        line_lock.acquire()
        if ready_tellers:
            my_teller = ready_tellers.pop(0)
        line_lock.release()
        if my_teller is None:
            time.sleep(0.001)  # brief yield before checking again

    # Remember which customer this teller is serving and wake the teller up.
    teller_customer_id[my_teller] = cid
    log("Customer", cid, "Teller", my_teller, "goes to this teller")
    teller_sem[my_teller].release()

    # Wait until the teller asks what we want to do.
    customer_sem[my_teller].acquire()
    log("Customer", cid, "Teller", my_teller, f"says they want a {txn}")

    # Fill in the shared slot and let the teller know it's ready.
    teller_transaction[my_teller] = txn
    transaction_sem[my_teller].release()

    # Wait for the teller to finish all the work.
    done_sem[my_teller].acquire()
    log("Customer", cid, "Teller", my_teller, "all done, heading out")

    # Let the teller know we've actually left the bank.
    leave_sem[my_teller].release()
    log("Customer", cid, "Customer", cid, "leaves bank")


# Main program: start all threads and wait for them to finish.
teller_threads = [threading.Thread(target=teller, args=(i,)) for i in range(NUM_TELLERS)]
customer_threads = [threading.Thread(target=customer, args=(i,)) for i in range(NUM_CUSTOMERS)]

for t in teller_threads:
    t.start()

for c in customer_threads:
    c.start()

for c in customer_threads:
    c.join()

# Wake any tellers still blocking on teller_sem after all customers done
for i in range(NUM_TELLERS):
    teller_sem[i].release()

for t in teller_threads:
    t.join()

print("Bank closed.")