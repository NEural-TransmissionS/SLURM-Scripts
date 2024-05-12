# Setup Conda environment on SLURM cluster

## Install `Miniforge3`

By default FIT AI.Panther SLURM nodes doesn't have anaconda installed, and the default system python is laced with old packages (check `AI.Panther/pipdeptree.txt`). To setup a conda environment on the SLURM cluster, follow the steps below:

1. Download and install the latest `miniforge3` distribution using [this guide](https://github.com/conda-forge/miniforge?tab=readme-ov-file#unix-like-platforms-mac-os--linux). Followed is the copy of the commands used:

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

2. Run the following command to activate the conda environment (in login node), or exit and re-login SSH to activate the conda environment:

```bash
source ~/.bashrc
```

## Create a new conda environment

### Create a new conda environment from scratch

`miniforge3` uses `mamba` as the package manager, which is a faster version of `conda`. To create a new conda environment, run the following command:

```bash
ENV_NAME="<env_name>"
PYTHON_VERSION="<python_version>"
mamba create -n $ENV_NAME python=$PYTHON_VERSION
mamba activate $ENV_NAME
```

Usually, it's fine to run this on login node (what you are interfacing with right after SSH'ing in). However, it is recommended to run this on a SLURM for a couple of reasons:
- The login node is shared among all users, and running heavy computation on it can slow down the system for everyone.
- Some packages require a GPU to install, and the login node doesn't have a GPU.

### Create a new conda environment from scratch using SLURM node

Here is a SLURM `srun` command to "SSH" into a SLURM node with a GPU (on partition `gpu1`) for 1 hour. Replace the `--time` flag with the desired time in the format "days-hours:minutes:seconds"

```bash
srun --partition=gpu1 --ntasks-per-node=1 --time=01:00:00 --pty bash -i
```

You will see something like this:

```bash
groups: cannot find name for group ID 10000
groups: cannot find name for group ID 10010
groups: cannot find name for group ID 10018
groups: cannot find name for group ID 10065
groups: cannot find name for group ID 10130
groups: cannot find name for group ID 10137
groups: cannot find name for group ID 10143
groups: cannot find name for group ID 10148
groups: cannot find name for group ID 10150
groups: cannot find name for group ID 10151
groups: cannot find name for group ID 10262
groups: cannot find name for group ID 10290
(base) I have no name!@gpu01:~$
```

These errors are normal and can be ignored. Proceed to run the mamba command like [above](#create-a-new-conda-environment-from-scratch) to create a new conda environment using SLURM node resources instead of login node.

### Create a new conda environment from an existing environment file

If you have an existing environment file, you can create a new conda environment from it. For example, if you have an environment file `environment.yml`, run the following command (replace `--partition=short` with `gpu1` if installation requires a GPU):

```bash
srun --partition=short mamba env create -y --file environment.yml
```