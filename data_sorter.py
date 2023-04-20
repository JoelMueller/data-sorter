import tkinter as tk
from tkinter import ttk
import pandas as pd

import config
import csv_helpers


class DataSorter:
    def __init__(self):
        self.table = csv_helpers.read_csv(config.input_file)
        self.filters = csv_helpers.read_csv(config.filters_file)
        self.number_of_rows = self.table.shape[0]
        self.rows_processed = 0
        self.new_tag = ""

        self.setup_gui(self.number_of_rows)

        self.start()

    def setup_gui(self, number_of_rows: int):
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

        self.amount_label = tk.Label(self.amount_frame, text=(config.amount_str + ':'),
                                     anchor="w", width=12)
        self.who_label = tk.Label(self.who_frame, text=(config.filter_who_str + ':'),
                                  anchor="w", width=12)
        self.what_label = tk.Label(self.what_frame, text=(config.filter_what_str + ':'),
                                   anchor="w", width=12)
        self.tag_label = tk.Label(self.tag_frame, text=(config.filter_tag_str + ':'),
                                  anchor="w", width=12)

        self.who_text = ""
        self.what_text = ""
        self.tag = tk.StringVar(self.window)
        self.tag.set(config.tags[0])

        self.amount = tk.Label(self.amount_frame, anchor="w")
        self.who = tk.Entry(self.who_frame, width=100)
        self.what = tk.Entry(self.what_frame, width=100)
        self.tag_menu = tk.OptionMenu(self.tag_frame, self.tag, *config.tags)

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
            self.main_frame, text="Start", command=self.start)
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

    def start(self):
        self.rows_processed = 0

        for row_index, row in self.table.iterrows():
            who, what, amount = csv_helpers.get_entries(
                row, [config.who_str, config.what_str, config.amount_str])
            self.process_row(row_index, who, what, amount)

            self.update_process()

        csv_helpers.write_csv(self.table, config.output_file)
        csv_helpers.write_csv(self.filters, config.filters_file)

        self.set_info_text("Done")

    def process_row(self, row_index: int, who, what, amount):
        tag_for_row = ""
        for _, filter_row in self.filters.iterrows():
            filter_who = str(filter_row[config.filter_who_str])
            filter_what = str(filter_row[config.filter_what_str])
            tag = filter_row[config.filter_tag_str]
            if filter_who in who or filter_what in what:
                tag_for_row = tag

        if tag_for_row == "":
            self.update_text_fields(who, what, amount)
            self.enable_buttons(True)

            self.window.wait_variable(self.wait_for_decision)

            tag_for_row = self.new_tag
            self.reset_filter_inputs()

        if tag_for_row == "":
            tag_for_row = config.tag_other_str

        self.table.at[row_index, config.filter_tag_str] = tag_for_row

    def update_process(self):
        self.rows_processed += 1
        self.progress_bar["value"] = self.rows_processed
        self.set_info_text("%i/%i" %
                           (self.rows_processed, self.number_of_rows))
        self.window.update()

    def add_filter(self):
        self.new_tag = self.tag.get()
        what = self.what.get()
        who = self.who.get()
        new_filter = {config.filter_tag_str:  [self.new_tag]}
        if who != "":
            new_filter[config.filter_who_str] = [self.who.get()]
        if what != "":
            new_filter[config.filter_what_str] = [self.what.get()]
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


if __name__ == "__main__":
    window = DataSorter()
