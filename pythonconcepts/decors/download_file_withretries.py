import os
import sys
import uuid
import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
import urllib3.exceptions


@retry(
    retry=(
        retry_if_exception_type(httpx.HTTPError) |
        retry_if_exception_type(urllib3.exceptions.HTTPError)
    ),
    stop=stop_after_attempt(10),
    wait=wait_fixed(60),
)
def download_file(*, url, path, client=None):
    """
    Atomically download a file from ``url`` to ``path``.

    If ``path`` already exists, the file will not be downloaded again.
    This means that different URLs should be saved to different paths.

    This function is meant to be used in cases where the contents of ``url``
    is immutable -- calling it more than once should always return the same bytes.

    Returns the download path.

    """
    # If the URL has already been downloaded, we can skip downloading it again.
    if os.path.exists(path):
        print("path exists")
        return path

    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    if client is None:
        client = httpx.Client()

    try:
        with client.stream("GET", url) as resp:
            resp.raise_for_status()

            # Download to a temporary path first.  That way, we only get
            # something at the destination path if the download is successful.
            #
            # We download to a path in the same directory so we can do an
            # atomic ``os.rename()`` later -- atomic renames don't work
            # across filesystem boundaries.
            tmp_path = f"{path}.{uuid.uuid4()}.tmp"
            print(f'Temp path is {tmp_path}')

            with open(tmp_path, "wb") as out_file:
                for chunk in resp.iter_raw():
                    out_file.write(chunk)

    # If something goes wrong, it will probably be retried by tenacity.
    # Log the exception in case a programming bug has been introduced in
    # the ``try`` block or there's a persistent error.
    except Exception as exc:
        print(exc, file=sys.stderr)
        raise

    os.rename(tmp_path, path)
    return path


if __name__ == '__main__':
    # download_file(*, url, path, client=None)
    # https://alexwlchan.net/2020/04/downloading-files-with-python/

    url1 = 'https://www.briandunning.com/sample-data/uk-500.zip'
    # the file test.zip should not already exist.
    # Won't download if the file exists.
    # download to a temporary path first, then an atomic rename to the final path.
    # If there’s a file at the final path, then it’s the complete file – it will never be something that’s only partially downloaded.
    path1 = '/Users/sbommireddy/Documents/test.zip'
    download_file(url=url1, path=path1)
