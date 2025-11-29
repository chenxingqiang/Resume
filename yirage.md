YiRage Persistent Kernel: Compiling LLMs into a MegaKernel

About
YiRage Persistent Kernel (MPK) is a compiler and runtime system that automatically transforms LLM inference into a single megakernel—a fused GPU kernel that performs all necessary computation and communication within a single kernel launch. This end-to-end GPU fusion approach reduces LLM inference latency by 1.2× to 6.7×, all while requiring minimal developer effort.

Quick Installation
The fastest way to try MPK is to install it directly from source:

git clone --recursive  http://gitlab-repo.yizhu.local/johnson.chen/yica-yirage.git
cd yirage
pip install -e . -v
export YIRAGE_HOME=$(pwd)



Quickstart
YiRage allows you to compile LLMs from the Hugging Face model zoo into a megakernel using just a few dozen lines of Python—mainly to define the kernel’s inputs and outputs. See this demo script that compiles the Qwen3-8B model into a megakernel.
We start by running the demo with native Triton and FlashInfer kernels:

python demo/qwen3/demo.py


To compile and execute the megakernel using MPK:

python demo/qwen3/demo.py --use-yirage


To enable profiling (which visualizes the execution timeline of each task):

python demo/qwen3/demo.py --use-yirage --profiling



How MPK Works
Once you've imported the YiRage package, you can instantiate a persistent kernel using the following API:

import yirage as yr
mpk = yr.PersistentKernel(
    world_size=world_size,
    mpi_rank=rank,
    num_workers=96,
    num_local_schedulers=48,
    num_remote_schedulers=0,
    meta_tensors=[step, tokens],
    profiler_tensor=profiler_tensor,
)




world_size and mpi_rank: number of GPUs and current GPU rank.

num_workers, num_local_schedulers, num_remote_schedulers: the number of workers, local schedulers, and remote schedulers. They must match the number of physical SMs (num_workers + (num_local_schedulers + num_remote_schedulers) / 4).
The megakernel currently requires two meta tensors: step is an array of integer tracking the current decoding step, and is incremented by MPK after each decoding iteration; tokens is a tensor of shape [num_requests, seq_length] storing prompts and MPK generated tokens.

To attach an existing PyTorch.Tensor:

x = mpk.attach_input(torch_tensor=torch_tensor, name="torch_tensor_name")




name is used by MPK to refer to the tensor in the generated megakernel in CUDA.

To allocate a new tensor:

y = mpk.new_tensor(
    dims=(batch_size, hidden_size),
    dtype=yr.bfloat16,
    name="embed_out",
    io_category="cuda_tensor",
)




dims and dtype specify the dimensions and data type of the tensor.

name is used by MPK to refer to this new tensor in the megakernel.

io_category indicates how the tensor is allocated and must be cuda_tensor or nvshmem_tensor (the latter is required for remote GPU access, e.g., during all-reduce).


Defining the Computation Graph
You can compose the LLM’s computation graph by chaining fused operations. For example: rmsnorm_linear_layer fuses an RMSNorm layer and a Linear layer in the megakernel.

mpk.rmsnorm_linear_layer(
    input=x,
    weight_norm=w_norm,
    weight_linear=w_qkv,
    output=attn_in,
    grid_dim=(96, 1, 1),
    block_dim=(128, 1, 1),
)




weight_norm and weight_linear are the weight tensors for RMSNorm and Linear.

input and output are the input and output tensors of this fused layer.

grid_dim and block_dim specifies the number of thread blocks (i.e., number of tasks in the task graph) and number of thread within each thread block. To minimize latency, it is suggested that the total number of thread blocks is a multiplier of the number of workers to avoid outliers.


Compilation & Execution
Once the computation graph is defined, compile it with:

mpk.compile()


Then, run the optimized megakernel as:

mpk()



License
YiRage uses Apache License 2.0.