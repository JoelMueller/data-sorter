import pandas as pd

import config
import csv_helpers

table = csv_helpers.read_csv(config.input_file)
filters = csv_helpers.read_csv(config.filters_file)


def process_row(row_index: int, who, what, amount):
    tag_for_row = ""
    for _, filter_row in filters.iterrows():
        filter_who = str(filter_row[config.filter_who_str])
        filter_what = str(filter_row[config.filter_what_str])
        tag = filter_row[config.filter_tag_str]
        if filter_who in who or filter_what in what:
            tag_for_row = tag

    if tag_for_row == "":
        tag_for_row = config.tag_other_str

    table.at[row_index, config.filter_tag_str] = tag_for_row


if __name__ == "__main__":
    for row_index, row in table.iterrows():
        who, what, amount = csv_helpers.get_entries(
            row, [config.who_str, config.what_str, config.amount_str])
        process_row(row_index, who, what, amount)

    csv_helpers.write_csv(table, config.output_file)
