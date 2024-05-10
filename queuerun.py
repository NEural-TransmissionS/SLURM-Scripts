"""
Parallel/concurrent execution of commands using a process pool and dynamic GPU allocation.

Usage:
1. Define the commands to be executed in the `commands` array.
2. Set the desired `pool_size` based on the number of available GPUs (usually 4).
3. Run the script.

The script will distribute the execution of commands across multiple worker processes,
with each process assigned a unique GPU device using CUDA_VISIBLE_DEVICES.
"""

import os
import subprocess
from multiprocessing import Pool, Manager

# Define an array of commands to execute
# example print hello world
COMMANDS = [
    "echo Hello World 1",
    "echo Hello World 2",
    "echo Hello World 3",
    "echo Hello World 4",
    "echo Hello World 5", 
]

# Create a process pool with a limited number of worker processes
POOL_SIZE = 4  # Set this to the number of available GPUs

# Function to execute a command with dynamic CUDA_VISIBLE_DEVICES
def execute_command(command, gpu_queue, gpu_lock):
    with gpu_lock:
        cuda_device = gpu_queue.get()
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = str(cuda_device)
    subprocess.run(command, shell=True, env=env)
    with gpu_lock:
        gpu_queue.put(cuda_device)


if __name__ == "__main__":
    manager = Manager()
    gpu_queue = manager.Queue()
    gpu_lock = manager.Lock()

    # Initialize the GPU queue with available GPU indices
    for i in range(POOL_SIZE):
        gpu_queue.put(i)

    with Pool(processes=POOL_SIZE) as pool:
        pool.starmap(execute_command, [(cmd, gpu_queue, gpu_lock) for cmd in COMMANDS])