![Employee Records Image](images/employees.jpg)

# Employee Records
A simple python script to ingest employee record CSVs, parse, and write a better-formatted output file.

## Problem

 A new HR system requires that employee records be stored differently. Currently, the records are stored in many .csv files with the following format:

```text
Emp ID,Name,DOB,SSN,State
214,Sarah Simpson,1985-12-04,282-01-8166,Florida
15,Samantha Lara,1993-09-08,848-80-7526,Colorado
411,Stacy Charles,1957-12-20,658-75-8526,Pennsylvania
```

Now, they need to be stored like this:

```text
Emp ID,First Name,Last Name,DOB,SSN,State
214,Sarah,Simpson,12/04/1985,***-**-8166,FL
15,Samantha,Lara,09/08/1993,***-**-7526,CO
411,Stacy,Charles,12/20/1957,***-**-8526,PA
```

## Data Structure
The data is contained in two .csv files with the above mentioned format. We will need to combine information from both and produce a single .csv in the new format.

## Strategy
The data will need to be ingested, unpacked into an array (a list of lists, each inner list representing a row of data). Then, a series of fixes will need to be applied.
* Splitting first and last name into seperate fields
* Changing date format from yyyy-mm-dd to yyyy/mm/dd
* Hiding all but last 4 digits of SSN
* Changing state names to abbreviations
    * In order to avoid reinventing the wheel, there exists a state name abbreviation dictionary online at [Python Dictionary for State Abbreviations](https://gist.github.com/afhaque/29f0f4f37463c447770517a6c17d08f5)

## Script
### Exploration
After identifying the filepaths for the input data and packaging them in a list for iteration, the function `shown()` was written in order to explore the headers and first few rows of data.

A few notes about `shown()`
* It contains an outer loop to iterate over files in the `filelist`, and an inner loop to iterate over rows in a single file. 
* The `os` module's `path.join()` function is used to construct the filepaths with the appropriate directory seperators for the user's OS.
* A counter is initialized at the beginning of the function, and incremented as the inner loop iterates through rows in a file.
    * When the counter equals the supplied argument to the function, it stops printing rows
* A `with` statement is used in tandem with the `open()` function to ensure the file is closed after reading
* The `csv` module's `reader()` function is used to construct an iterable 'reader' object, with each element in the iterable being a row from the csv. Each of these elements is a list, and columns from the row can be accessed by row slicing.

`shown()` was used to explore the headers and first few rows of data from each file to ensure they were consistently formatted.

### Counting Employees
In order to determine the total number of employees, `countemps()` was written to iterate over rows in each file, incrementing a counter with each row. It has a similar structure to `shown()`, with an outer loop iterating over files and an inner loop iterating over rows in each file. The differences are:
* In addition to the inner loop row counter in `shown()`, there is an outer loop counter, `totcount`, that keeps count of all rows in total. It is initialized as zero at the beginning of the function, and is updated after an individual file is iterated over.
* In the inner loop, an `if` statement allows the loop to skip over header rows, by testing whether the row's first element equals 'Emp ID', the first column header.
* `totcount` is returned to give a total count of rows in all files

### Unpacking Data for Manipulation
The `unpack()` function serves to iterate through the .csv files, then rows in those .csv files, in order to store each row as a list. Those lists are then stored in a master list, `rawarray`, so that they can be manipulated more easily. A few notes on `unpack()`:
* The function is structured like `countemps()`, iterating through files, then rows using `csv` module's reader object constructor, and skipping headers.
* Each row is read and stored in `rawarray`
* The function returns this array for later manipulation

### Data Modification
The rest of the functions:
* `splitname()`
* `splitdate()`
* `hidessn()`
* `convstate()`

All serve to select an element from a row in the array, pop it out, store it, modify it, and insert the modified data back into the row at the same position. All iterate over the rows in the array.

A note about `splitname()`
* This function splits the 'firstname lastname' format string into a list on the ' ' delimiter. Each element from the list is then appended in the for loop on line 149. After all rows have been modified, the modified array is returned to be fed into the next step.

A note about `splitdate()`:
* This function works similarly to `splitname()`, splitting the '-' delimited yyyy-mm-dd format into a three-element list, joining elements of that list into a string delimited by '/' using `join()`, and inserting the resulting modified string into the proper position in the row. After all rows have been modified, the modified array is returned to be fed into the next step.

A note about `hidessn()`:
* This function works like the above two functions, splitting the SSN on the '-' delimiter, appending asterisks to replace the first 5 digits, and appending the true last four digits to a list. That list is then joined with a '-' delimiter, and inserted into the row it was removed from . After all rows have been modified, the modified array is returned to be fed into the next step.

A note about `convstate()`:
* This function works by removing and storing the long-form state name, and comparing it to each key in the state name abbreviation dictionary found at the link above. When a match is found, the corresponding value (abbreviation) is retrieved, and inserted into the row at the proper position. After all rows have been modified, the modified array is returned to be fed into the next step.

### Printing Results to Console and File
After all above modifications have been made to the array, A new header row is stored as a list to reflect the new column names. `os` module's `path.join()` function is used to construct a filepath with the appropriate directory seperators, and an empty .txt file is opened for writing.

`csv` module's writer constructor is used to first write the new header row to file, followed by each row of the modified array using a for loop. The output file can be viewed in the output_data folder of the repo.