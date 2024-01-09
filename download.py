import functools
import pathlib
import shutil
import requests
from tqdm.auto import tqdm
import os


def download_model(url, filename=None):
    if not filename:
        filename = os.path.join("models", url.split("/")[-1])
    r = requests.get(
        format_url(url),
        stream=True,
        allow_redirects=True,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    if r.status_code != 200:
        r.raise_for_status()  # Will only raise for 4xx codes, so...
        raise RuntimeError(f"Request to {url} returned status code {r.status_code}")
    file_size = int(r.headers.get("Content-Length", 0))

    path = pathlib.Path(filename).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    desc = "(Unknown total file size)" if file_size == 0 else ""
    r.raw.read = functools.partial(
        r.raw.read, decode_content=True
    )  # Decompress if needed
    with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
        with path.open("wb") as f:
            shutil.copyfileobj(r_raw, f)


def format_url(url):
    repo_name = url.split("/")[3] + "/" + url.split("/")[4]
    model_name = url.split("/")[-1]
    return f"https://huggingface.co/{repo_name}/resolve/main/{model_name}?download=true"
