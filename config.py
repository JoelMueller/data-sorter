from dataclasses import dataclass
from typing import List

who_str = "Recipient"
what_str = "Purpose"
amount_str = "Amount (USD)"
filter_who_str = "Recipient"
filter_what_str = "Purpose"
filter_tag_str = "Category"
tag_other_str = "Other"
tags = ["Cost of Living",
        "Recreation",
        "Rent"]


@dataclass
class DataSorterConfig:
    csv_encoding: str
    csv_separator: str

    input_file: str
    output_file: str
    filters_file: str

    who_str: str
    what_str: str
    amount_str: str
    filter_who_str: str
    filter_what_str: str
    filter_tag_str: str
    tag_other_str: str
    tags: List[str]
