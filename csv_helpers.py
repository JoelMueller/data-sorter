import pandas as pd


def read_csv(input_file, config):
    return pd.read_csv(
        input_file, engine='c', encoding=config.csv_encoding, sep=config.csv_separator)


def write_csv(data_frame, output_file, config):
    data_frame.to_csv(output_file, index=False,
                      encoding=config.csv_encoding, sep=config.csv_separator)


def get_entries(row, names):
    def get_entry(name):
        return row[name] if pd.notnull(row[name]) else ""

    return [get_entry(name) for name in names]
