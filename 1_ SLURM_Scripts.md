# Running SLURM script on AI.Panther

As simple as:

```bash
sbatch <script_name>.sh
```

All `#SBATCH` directives defined at the beginning of the SLURM script can be overridden by passing the flag to the `sbatch` command. For example, to override the `--job-name` directive in the script (default to `NETS_Script`), run:

```bash
sbatch --job-name=<desired_job_name> <script_name>.sh
```

# Using multiple GPUs for multiple training jobs

So AI.Panther `slurm.conf` and `gres.conf` is totally busted. If you schedule `gpus-per-node=1` for multiple jobs, it will only runs job on the first GPU. To run multiple jobs on multiple GPUs, you need to schedule `gpus-per-node=4` and then use `CUDA_VISIBLE_DEVICES` to specify which GPU to use.

Provided in this repository is a `queuerun.py` script that runs multiple training jobs on multiple GPUs. To use it, add a list of commands to run in the `queuerun.py` script and then run the `sbatch` command:

```bash
sbatch slurm_all_gpu.sh
```

# Using all 4 GPUs for PyTorch Distributed Data Parallel

Make sure the training script is using PyTorch's Distributed Data Parallel (DDP) module. Then, add these lines replacing `python queuerun.py` in the `slurm_all_gpu.sh` SLURM script:

```bash
# Output all NCCL debug info to stdout
export NCCL_DEBUG=INFO
export NCCL_DEBUG=WARN
# Some NCCL flags for multi-node training (in case GPU doesn't support feature)
export NCCL_IB_DISABLE=1
export NCCL_P2P_DISABLE=1
export CUDA_LAUNCH_BLOCKING=1

# Run the training script (replace with your training script command and options)
torchrun --nproc_per_node ${N_PROC:=4} train.py
```