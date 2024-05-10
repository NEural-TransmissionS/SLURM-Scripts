# Setup Conda environment on SLURM cluster

By default FIT AI.Panther SLURM nodes doesn't have anaconda installed, and the default system python is laced with old (check AI.Panther/pipdeptree.txt). To setup a conda environment on the SLURM cluster, follow the steps below:

1. Download and install the latest `miniforge3` distribution using [this guide](https://github.com/conda-forge/miniforge?tab=readme-ov-file#unix-like-platforms-mac-os--linux). Followed is the copy of the commands used:

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

2. Use `cat ~/.bashrc` content, if the follow block doesn't exists then add the conda path to your `.bashrc` file:

```bash
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home1/vnguyen2014/mambaforge/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home1/vnguyen2014/mambaforge/etc/profile.d/conda.sh" ]; then
        . "/home1/vnguyen2014/mambaforge/etc/profile.d/conda.sh"
    else
        export PATH="/home1/vnguyen2014/mambaforge/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
```

3. Run the following command to activate the conda environment:

```bash
source ~/.bashrc
```

# Create a new conda environment

## Create a new conda environment from scratch

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

Here is a SLURM `srun` command to "SSH" into a SLURM node with a GPU (on partition `gpu1`) for 1 hour. Replace the `--time` flag with the desired time in the format "days-hours:minutes:seconds"

```bash
srun --partition=gpu1 --ntasks-per-node=1 --time=01:00:00 --pty bash -i
```

Proceed to run the `mamba create` and `mamba install` command on the SLURM node.