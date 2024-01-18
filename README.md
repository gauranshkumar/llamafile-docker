# Dockerised [llamafile](https://github.com/Mozilla-Ocho/llamafile)

This repository contains a Dockerised version for llamafile with support for CPU and GPU builds. The `Dockerfile.gpu` is based on the [official CUDA image](https://hub.docker.com/r/nvidia/cuda/).

## Utility Scripts
The `scripts` directory contains a utility script to download models from the hugging face model hub and run the docker image. The script can be used as follows:
1. Download a model from the hugging face model hub:
```bash
python scripts/main.py download https://huggingface.co/jartine/llava-v1.5-7B-GGUF/blob/main/llava-v1.5-7b-Q4_K.gguf
```
> To pass any raw arguments to the `llamafile` executable, use the `--extra-args` flag with `run` and then any flag you want to pass after it. 


## Docker Hub
The docker images are available on Docker Hub at [gauransh/llamafile-docker](https://hub.docker.com/r/gauransh/llamafile-docker). The images are tagged as `latest` and `latest-gpu` for CPU and GPU builds respectively.
Currently, the latest refers to `v0.6` of llamafile [release](https://github.com/Mozilla-Ocho/llamafile/releases/tag/0.6).

## Pre-requisites
1. Install [Docker](https://docs.docker.com/get-docker/) on your host machine.
> **Only needed for GPU usage**
2. Install [nvidia-container-toolkit](https://github.com/NVIDIA/nvidia-container-toolkit) on your host machine.


## Usage
1. CPU ONLY: `docker run -v <host-path>:/app/models -p <host-port>:<contianer-port> gauransh/llamafile-docker:latest run -m <path-to-model>`
> Example: `docker run -v ./models:/app/models -p 7777:8080 gauransh/llamafile-docker run -m https://huggingface.co/TheBloke/Code-13B-GGUF/blob/main/code-13b.Q2_K.gguf`

2. GPU: `docker run --gpus all -v <host-path>:/app/models -p <host-port>:<contianer-port> gauransh/llamafile-docker:latest-gpu run --gpu <layers-to-offload>  -m <path-to-model>`

>  Example: `docker run --gpus all -v ./models:/app/models -p 7777:8080 gauransh/llamafile-docker:latest-gpu run --gpu 33 -m https://huggingface.co/TheBloke/Code-13B-GGUF/blob/main/code-13b.Q2_K.gguf`

> **Model Persistance**: The models weights are saved in the `/app/models` directory in the container. To persist the models, attach a volume to the container at this path. Check Usage above for an example.
 
## Script Usage:

```
python scripts/main.py -h          
usage: Llamafile Docker Utility [-h] {run,download} ...

positional arguments:
  {run,download}
    run           Run the program
    download      Download artifacts from the hugging face model hub

options:
  -h, --help      show this help message and exit
```

```
python scripts/main.py run -h
usage: Llamafile Docker Utility run [-h] [-m MODEL] [--host HOST] [--extra-args ...] [--gpu GPU]

options:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        The name of the model to run. E.g. url/path to model gguf. If not provided, the default model will be used.
  --host HOST           Specify the host address for the llamafile server
  --extra-args ...      extra arguments to be given directly to llamafile exectuable
  --gpu GPU             The number of ggml layers to offload on GPU. E.g. 1. If not provided, the default model will be used
```

```
python scripts/main.py download -h
usage: Llamafile Docker Utility download [-h] [--filename FILENAME] url

positional arguments:
  url                  The URL to download E.g. https://huggingface.co/jartine/llava-v1.5-7B-GGUF/blob/main/llava-v1.5-7b-Q4_K.gguf

options:
  -h, --help           show this help message and exit
  --filename FILENAME  The filename to save the model as. E.g. mixtral-8x7b-v0.1.Q2_K.gguf. If not provided, the filename will be inferred from the URL. and
                       saved in the models directory.
```


## Usage with OpenAI API
```python
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
    api_key = "sk-no-key-required"
)
completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[
        {"role": "system", "content": "You are ChatGPT, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests."},
        {"role": "user", "content": "Write a limerick about python exceptions"}
    ]
)
print(completion.choices[0].message)
```