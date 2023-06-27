from typing import Iterator


def chunks(data: list, n: int) -> Iterator[list]:
    """
    Yield successive n-sized chunks from l.
    :param l: list
    :param n: chunk size
    """
    for i in range(0, len(data), n):
        yield data[i:i + n]
