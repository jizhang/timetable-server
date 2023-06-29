from typing import Iterator, Sequence


def chunks(data: Sequence, n: int) -> Iterator[Sequence]:
    """
    Yield successive n-sized chunks from l.
    :param l: list
    :param n: chunk size
    """
    for i in range(0, len(data), n):
        yield data[i:i + n]
