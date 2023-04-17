import pandas as pd

import config

table = pd.read_csv(config.input_file, engine='c',
                    encoding=config.csv_encoding, sep=config.csv_separator)
filters = pd.read_csv(config.filters_file, engine='c',
                      encoding=config.csv_encoding, sep=config.csv_separator)

for i, row in table.iterrows():
    who = row[config.who_str]
    who = who if pd.notnull(who) else ""
    what = row[config.what_str]
    what = what if pd.notnull(what) else ""
    tag_for_row = ""
    for j, filter_row in filters.iterrows():
        filter_who = str(filter_row[config.filter_who_str])
        filter_what = str(filter_row[config.filter_what_str])
        tag = filter_row[config.filter_tag_str]
        if filter_who in who or filter_what in what:
            tag_for_row = tag
    if tag_for_row == "":
        tag_for_row = config.tag_other_str
    table.at[i, config.filter_tag_str] = tag_for_row

table.to_csv(config.output_file, index=False,
             encoding=config.csv_encoding, sep=config.csv_separator)
