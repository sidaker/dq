# hyper threading
# This program uses one CPU at most due to python's GIL.
import os
import threading

def cpu_waster():
    while True:
        pass


# display information about this process
print('\n Process ID:',os.getpid())
print('Thread Count:',threading.active_count())

for thread in threading.enumerate():
    print(thread)

# Starting 6 CPU wasters.
for i in range(6):
    threading.Thread(target=cpu_waster).start()

# Display information about these 6 threads.
# display information about this process
print('\n Process ID:',os.getpid())
print('Thread Count:',threading.active_count())

for thread in threading.enumerate():
    print(thread)
