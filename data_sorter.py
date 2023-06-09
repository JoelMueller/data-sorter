import tkinter as tk
from tkinter import ttk
import click
import pandas as pd

from config import Constants, DataSorterConfig
import csv_helpers


class DataSorter:
    def __init__(self, data_sorter_config):
        self.config = data_sorter_config

        self.table = csv_helpers.read_csv(self.config.input_file, self.config)
        self.filters = csv_helpers.read_csv(
            self.config.filters_file, self.config)
        self.number_of_rows = self.table.shape[0]
        self.rows_processed = 0

        self.who_text = ""
        self.what_text = ""
        self.new_tag = ""

        self.setup_gui(self.number_of_rows)

    def setup_gui(self, number_of_rows: int):
        # pylint: disable=too-many-statements

        self.window = tk.Tk()
        self.window.title("Data Sorter")

        # ====================================================================================
        # Filter inputs

        self.amount_frame = tk.Frame(self.window)
        self.who_frame = tk.Frame(self.window)
        self.what_frame = tk.Frame(self.window)
        self.tag_frame = tk.Frame(self.window)

        self.amount_frame.pack(side="top", fill="x", expand=True)
        self.who_frame.pack(side="top", fill="x", expand=True)
        self.what_frame.pack(side="top", fill="x", expand=True)
        self.tag_frame.pack(side="top", fill="x", expand=True)

        self.amount_label = tk.Label(self.amount_frame, text=(Constants.AMOUNT_STR + ':'),
                                     anchor="w", width=12)
        self.who_label = tk.Label(self.who_frame, text=(Constants.FILTER_WHO_STR + ':'),
                                  anchor="w", width=12)
        self.what_label = tk.Label(self.what_frame, text=(Constants.FILTER_WHAT_STR + ':'),
                                   anchor="w", width=12)
        self.tag_label = tk.Label(self.tag_frame, text=(Constants.FILTER_TAG_STR + ':'),
                                  anchor="w", width=12)

        self.who_text = ""
        self.what_text = ""
        self.tag = tk.StringVar(self.window)
        self.tag.set(Constants.TAGS[0])

        self.amount = tk.Label(self.amount_frame, anchor="w")
        self.who = tk.Entry(self.who_frame, width=100)
        self.what = tk.Entry(self.what_frame, width=100)
        self.tag_menu = tk.OptionMenu(
            self.tag_frame, self.tag, *Constants.TAGS)

        self.clear_who_button = tk.Button(
            self.who_frame, text="Clear", command=self.clear_who)
        self.clear_what_button = tk.Button(
            self.what_frame, text="Clear", command=self.clear_what)

        self.reset_who_button = tk.Button(
            self.who_frame, text="Reset", command=self.reset_who)
        self.reset_what_button = tk.Button(
            self.what_frame, text="Reset", command=self.reset_what)

        self.amount_label.pack(side="left", padx=5, pady=5)
        self.who_label.pack(side="left", padx=5, pady=5)
        self.what_label.pack(side="left", padx=5, pady=5)
        self.tag_label.pack(side="left", padx=5, pady=5)

        self.amount.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self.who.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self.what.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self.tag_menu.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        self.clear_who_button.pack(side="left", padx=5, pady=5)
        self.clear_what_button.pack(side="left", padx=5, pady=5)

        self.reset_who_button.pack(side="left", padx=5, pady=5)
        self.reset_what_button.pack(side="left", padx=5, pady=5)

        # ====================================================================================
        # Start button & progress bar

        self.main_frame = tk.Frame(self.window)
        self.start_button = tk.Button(
            self.main_frame, text="Start", command=self.start_data_processing)
        self.progress_bar = ttk.Progressbar(self.main_frame, orient="horizontal", length=400,
                                            mode="determinate", maximum=number_of_rows)
        self.info = tk.Label(self.main_frame, width=8)

        self.start_button.pack(side="left", padx=5, pady=5)
        self.progress_bar.pack(side="left", padx=5, pady=5)
        self.info.pack(side="bottom", padx=5, pady=5)
        self.main_frame.pack(side="left")

        # ====================================================================================
        # Add & Skip button

        self.button_frame = tk.Frame(self.window)
        self.add_filter_button = tk.Button(self.button_frame, text="Add Filter",
                                           command=self.add_filter)
        self.skip_button = tk.Button(
            self.button_frame, text="Skip", command=self.skip)

        self.add_filter_button.pack(side="left", padx=5, pady=5)
        self.skip_button.pack(side="left", padx=5, pady=5)
        self.button_frame.pack(side="right")

        # ====================================================================================

        self.wait_for_decision = tk.BooleanVar(value=False)

        self.enable_buttons(False)

        self.window.mainloop()

    def start_data_processing(self):
        self.rows_processed = 0

        for row_index, row in self.table.iterrows():
            who, what, amount = csv_helpers.get_entries(
                row, [Constants.WHO_STR, Constants.WHAT_STR, Constants.AMOUNT_STR])
            self.process_row(row_index, who, what, amount)

            self.update_process()

        csv_helpers.write_csv(self.table, self.config.output_file, self.config)
        csv_helpers.write_csv(
            self.filters, self.config.filters_file, self.config)

        self.set_info_text("Done")

    def process_row(self, row_index: int, who, what, amount):
        tag_for_row = ""
        for _, filter_row in self.filters.iterrows():
            filter_who = str(filter_row[Constants.FILTER_WHO_STR])
            filter_what = str(filter_row[Constants.FILTER_WHAT_STR])
            tag = filter_row[Constants.FILTER_TAG_STR]
            if filter_who in who or filter_what in what:
                tag_for_row = tag

        if tag_for_row == "":
            self.update_text_fields(who, what, amount)
            self.enable_buttons(True)

            self.window.wait_variable(self.wait_for_decision)

            tag_for_row = self.new_tag
            self.reset_filter_inputs()

        if tag_for_row == "":
            tag_for_row = Constants.TAG_OTHER_STR

        self.table.at[row_index, Constants.FILTER_TAG_STR] = tag_for_row

    def update_process(self):
        self.rows_processed += 1
        self.progress_bar["value"] = self.rows_processed
        self.set_info_text(f"{self.rows_processed}/{self.number_of_rows}")
        self.window.update()

    def add_filter(self):
        self.new_tag = self.tag.get()
        what = self.what.get()
        who = self.who.get()
        new_filter = {Constants.FILTER_TAG_STR:  [self.new_tag]}
        if who != "":
            new_filter[Constants.FILTER_WHO_STR] = [self.who.get()]
        if what != "":
            new_filter[Constants.FILTER_WHAT_STR] = [self.what.get()]
        self.filters = pd.concat(
            [self.filters, pd.DataFrame(new_filter)], ignore_index=True)

        self.wait_for_decision.set(True)

    def skip(self):
        self.wait_for_decision.set(True)

    def set_info_text(self, text: str):
        self.info.config(text=text)

    def update_text_fields(self, who, what, amount):
        self.who_text = who
        self.reset_who()
        self.what_text = what
        self.reset_what()
        self.amount.config(text=amount)

    def enable_buttons(self, enable: bool):
        state = "normal" if enable else "disabled"
        self.add_filter_button.config(state=state)
        self.skip_button.config(state=state)

    def reset_filter_inputs(self):
        self.clear_who()
        self.clear_what()
        self.new_tag = ""

    def clear_who(self):
        self.who.delete(0, "end")

    def clear_what(self):
        self.what.delete(0, "end")

    def reset_who(self):
        self.clear_who()
        self.who.insert(0, self.who_text)

    def reset_what(self):
        self.clear_what()
        self.what.insert(0, self.what_text)


CONTEXT_SETTINGS = {"show_default": True,
                    "help_option_names": ['-h', '--help']}


@click.command("cli", context_settings=CONTEXT_SETTINGS)
@ click.option("--encoding", "-e", default="windows_1258", help="CSV encoding")
@ click.option("--separator", "-s", default=',', help="CSV separator")
@ click.option("--input-file", "-i", default="data/data.csv", help="Input CSV file")
@ click.option("--output-file", "-o", default="data/data_out.csv", help="Output CSV file")
@ click.option("--filters-file", "-f", default="data/filters.csv",
               help="CSV file containing the filters")
def cli(encoding, separator, input_file, output_file, filters_file):
    """Sort data into categories."""

    data_sorter_config = DataSorterConfig(
        csv_encoding=encoding,
        csv_separator=separator,
        input_file=input_file,
        output_file=output_file,
        filters_file=filters_file)

    DataSorter(data_sorter_config)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
