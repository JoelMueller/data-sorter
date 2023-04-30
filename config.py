from dataclasses import dataclass


class Constants:
    WHO_STR = "Recipient"
    WHAT_STR = "Purpose"
    AMOUNT_STR = "Amount (USD)"
    FILTER_WHO_STR = "Recipient"
    FILTER_WHAT_STR = "Purpose"
    FILTER_TAG_STR = "Category"
    TAG_OTHER_STR = "Other"
    TAGS = ["Cost of Living",
            "Recreation",
            "Rent"]


@dataclass
class DataSorterConfig:
    csv_encoding: str
    csv_separator: str

    input_file: str
    output_file: str
    filters_file: str
