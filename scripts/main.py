import argparse
import os
import subprocess
from urllib.parse import urlparse
from download import download_model


def call_llama(extra_args=None):
    try:
        # Execute the command, capture stdout and stderr
        command = " ".join(["/bin/sh", "./llamafile", *extra_args])
        print(command)
        result = subprocess.Popen(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        for line in result.stdout:
            print(line, end="")

    except subprocess.CalledProcessError as e:
        # An error occurred during the execution
        print("Error executing the command:")
        print(e.stderr)


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


# Create the top-level parser
parser = argparse.ArgumentParser(prog="Llamafile Docker Utility")

# Create the subparsers
subparsers = parser.add_subparsers(dest="command")

# Create the 'run' subparser
run_parser = subparsers.add_parser("run", help="Run the program")

# Create the 'download' subparser
download_parser = subparsers.add_parser(
    "download", help="Download artifacts from the hugging face model hub"
)

download_parser.add_argument(
    "url",
    type=str,
    help="The URL to download E.g. https://huggingface.co/jartine/llava-v1.5-7B-GGUF/blob/main/llava-v1.5-7b-Q4_K.gguf",
)

download_parser.add_argument(
    "--filename",
    type=str,
    required=False,
    help="The filename to save the model as. E.g. mixtral-8x7b-v0.1.Q2_K.gguf. If not provided, the filename will be inferred from the URL. and saved in the models directory.",
)

run_parser.add_argument(
    "-m",
    "--model",
    default="https://huggingface.co/jartine/llava-v1.5-7B-GGUF/blob/main/llava-v1.5-7b-Q4_K.gguf",
    help="The name of the model to run. E.g. url/path to model gguf. If not provided, the default model will be used.",
)

run_parser.add_argument(
    "--host",
    default="0.0.0.0",
    help="Specify the host address for the llamafile server",
)

run_parser.add_argument(
    "--extra-args",
    required=False,
    help="extra arguments to be given directly to llamafile exectuable",
    nargs=argparse.REMAINDER,
)

run_parser.add_argument(
    "--gpu",
    type=str,
    help="The number of ggml layers to offload on GPU. E.g. 1. If not provided, the default model will be used",
    default=None,
)

# Parse the command-line arguments
args = parser.parse_args()

# Handle the 'run' command
if args.command == "run":
    # TODO: Add code to handle the 'run' command

    if args.gpu is not None:
        if "--n-gpu-layers" or "-ngl" not in args.extra_args:
            if args.extra_args is None:
                args.extra_args = []
            args.extra_args.append("--gpu")
            args.extra_args.append("auto")
            args.extra_args.append("--n-gpu-layers")
            args.extra_args.append((args.gpu or "1"))
    if args.model:
        default_args = [
            "--host",
            args.host,
            "--nobrowser",
        ]
        default_args = default_args + (args.extra_args or [])
        u = os.path.join("models", args.model.split("/")[-1])
        print(u)
        if os.path.isfile(args.model) or os.path.isfile(u):
            print("Model exists loading model")
            default_args = [
                "-m",
                u,
                *default_args,
            ]
            call_llama(extra_args=default_args)
        else:
            print("Model does not exist")
            print("Downloading model")
            if is_url(args.model):
                default_args = ["-m", download_model(args.model), *default_args]
                call_llama(extra_args=default_args)
            else:
                print("Invalid url")
                print("Please provide a url to download the model")
                exit(1)
    print(args.extra_args)

# Handle the 'download' command
elif args.command == "download":
    # TODO: Add code to handle the 'download' command
    print(f"Saved model at {download_model(args.url, args.filename)}")
