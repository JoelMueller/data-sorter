# DataSorter

DataSorter is a simple tool for quickly sorting large amounts of data into categories. It scans a data table row by row and, based on a set of filters, assigns a tag to each row. If no filter matches a given row, it lets the user add a new filter with a few simple clicks.

## Dependencies
---

DataSorter requires python 3.7 or newer as well as the following python packages:
* click
* pandas
* tkinter

## Usage
---

```
Usage: data_sorter.py [OPTIONS]

  Sort data into categories.

Options:
  -e, --encoding TEXT      CSV encoding  [default: windows_1258]        
  -s, --separator TEXT     CSV separator  [default: ,]
  -i, --input-file TEXT    Input CSV file  [default: data/data.csv]     
  -o, --output-file TEXT   Output CSV file  [default: data/data_out.csv]
  -f, --filters-file TEXT  CSV file containing the filters  [default:   
                           data/filters.csv]
  -h, --help               Show this message and exit.
```

## Example
---

Say you have a list of wire transfers from and into your bank account, and you want to get an overview of how you are spending your money each month. For this, you want to group the long list of wire transfers into a small number of categories, such as _Cost of Living_ or _Rent_. Instead of going through the list and tagging each entry manually, you can use DataSorter to add categories automatically.

Let's say this is the list of wire transfers:

|Date    |Recipient |Purpose                              |Amount (USD)|
|--------|----------|-------------------------------------|------------|
|19/11/20|Superstore|Thank you for shopping at Superstore!|83.62       |
|18/11/20|Torgot    |Thank you for shopping at Torgot!    |72.48       |
|15/11/20|PayPal    |Your monthly Netflix subscription    |9.99        |
|7/11/20 |Torgot    |Thank you for shopping at Torgot!    |143.35      |
|01/11/20|John Doe  |Monthly Rent                         |941.5       |

You can then define a list of filters that search for a match in the _Recipient_ or the _Purpose_ field and assigns the respective category.

|Recipient |Purpose   |Category                             |
|----------|----------|-------------------------------------|
|Superstore|          |Cost of Living                       |
|          |Netflix   |Recreation                           |
|          |Rent      |Rent                                 |

Note that there is no matching filter for the second wire transfer. If this happens, DataSorter prompts you to add a new filter. It populates the text input boxes with the according cells from the data table for you to modify before adding a new filter:

![screenshot_add_new_filter](https://user-images.githubusercontent.com/24793877/233482084-623e534a-bb61-4cf6-bd67-9a7521af7143.png)

Clicking _Add Filter_ will then add a new filter to the list which will be written to the respective CSV file at the end.

This makes sifting through large amounts of data, adding new filters where needed, fast and simple.

This is the result of running DataSorter on the example input:

|Date    |Recipient |Purpose                              |Amount (USD)|Category      |
|--------|----------|-------------------------------------|------------|--------------|
|19/11/20|Superstore|Thank you for shopping at Superstore!|83.62       |Cost of Living|
|18/11/20|Torgot    |Thank you for shopping at Torgot!    |72.48       |Cost of Living|
|15/11/20|PayPal    |Your monthly Netflix subscription    |9.99        |Recreation    |
|7/11/20 |Torgot    |Thank you for shopping at Torgot!    |143.35      |Cost of Living|
|01/11/20|John Doe  |Monthly Rent                         |941.5       |Rent          |