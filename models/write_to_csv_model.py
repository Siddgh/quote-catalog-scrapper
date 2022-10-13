from dataclasses import dataclass


@dataclass
class CSVWriterModel:
    year: str
    movie: str
    quote: str
    author: str
    tags: str
    status: str
