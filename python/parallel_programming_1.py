'''
Threads vs  Process.
Flynn's taxanomy - SIMD, SISD, MISD,MIMD(Multiple Instructions Multiple data)
SPMD - Single Program Multiple Data
MPMD
Shared Vs Distributed memory.
UMA vs NUMA (Non uniform memory access)
SMP architecture -> 2 or more idenentical processors connected to single shared main memory.
each core has its own cache.
Handling cache coherency

process vs thread.
Each process is independent and has its own address space in memory.
Its an independent instance of a running program.
OS manages the processes.

With in each process  there can be multiple threads.
threads are a subset of process. basic units an OS manages.
threads with in the same process share the same memory space.

Communicating between threads of different processes?
Sharing resources between different processes?
There's no easy way.You need to use IPC(Inter process Communication)
like sockets and pipes, shared memory, RPC(Remote Procedure calls?)
Using RPC, you can make a process send data to a port  and the other process can listen on that port and read the data.

Threads vs Processes.
Threads are light weight.
Easy/faster for OS to switch between threads than processes.

Concurrency vs Parallel execution

Concurrent execution with single processor-
Each process takes turn and executes concurrently.

GIL- Global Interpreter Lock(GIL) limits python to execute one thread at a time.
C Python has GIL.
Jython and IronPython whcih are java and .NET based dont have GIL.

I/O -Bound Applications
GIL is not a bottle neck and use the Python threading module.
Example program that downloads files in paralle.

CPU - Bound Applications
GIT can impact negatively performance.
Use Python multiprocessing package.
Each process will be its own instance of python's interpreter and will have its own GIL.
Downiside  -  Communication between processes.

'''
