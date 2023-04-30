import pandas as pd


def read_csv(input_file, config):
    return pd.read_csv(input_file, engine='c', encoding=config.csv_encoding, sep=config.csv_separator)


def write_csv(data_frame, output_file, config):
    data_frame.to_csv(output_file, index=False,
                      encoding=config.csv_encoding, sep=config.csv_separator)


def get_entries(row, names):
    entries = []
    for name in names:
        entry = row[name]
        entry = entry if pd.notnull(entry) else ""
        entries.append(entry)

    return entries
