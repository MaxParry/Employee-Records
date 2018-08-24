import os
import csv

# dictionary of state abbreviations used to transform data to uniformity
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

# identify locations and names of source files
sourcedirectory = 'input_data'
file1 = 'employee_data1.csv'
file2 = 'employee_data2.csv'

# package source filenames in a list for iteration
filelist = [file1, file2]


# for exploration, prints n number of rows in each file

def shown(n):
    # iterate over files
    for afile in filelist:
        # initialize row counter
        counter = 0
        # construct filepath using appropriate directory seperators
        path = os.path.join(sourcedirectory, afile)
        # open file for reading
        with open(path, 'r', newline='') as f:
            # csv module allows for construction of reader objects
            # reader is an iterable with rows from csvs as elements
            reader = csv.reader(f, delimiter=',')
            # iterate over rows in csv
            for row in reader:
                # increment row counter
                counter = counter + 1
                print(row)
                # stop printing rows when counter larger than argument
                if counter >= n:
                    print('')
                    break

# countemps() returns total number of employees, skipping headers

def countemps():
    # initialize counter for all files
    totcount = 0
    # iterate over files
    for afile in filelist:
        # initialize counter for rows in individual file
        counter = 0
        # construct filepath using appropriate directory seperators
        path = os.path.join(sourcedirectory, afile)
        # open file for reading
        with open(path, 'r', newline='') as f:
            # construct reader object for iterating through rows in csv
            reader = csv.reader(f, delimiter=',')
            # iterate through rows
            for row in reader:
                # if header row, skip
                if row[0] == 'Emp ID':
                    pass
                # if not header row, increment counter
                else:
                    counter = counter + 1
        # update total count after all rows in individual file counted
        totcount = totcount + counter
    return totcount

# unpacks employee data into an array, same as above but instead of
# counting, it appends the row (itself a list) to rawarray (list of lists)

def unpack():
    # initialize list to hold inner lists
    rawarray = []
    for afile in filelist:
        path = os.path.join(sourcedirectory, afile)
        with open(path, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[0] == 'Emp ID':
                    pass
                else:
                    rawarray.append(row)
    return rawarray

# ingest data into array
rawarray = unpack()

# splitname() pops off the employee name, splits it on space,
# and inserts it back into the same region of the list
def splitname():
    # iterate over rows (employees)
    for row in rawarray:
        # pop (remove and return) 1st element in row (row is a list)
        wholename = row.pop(1)
        # split name string into 2-element list [firstname, lastname]
        namelist = wholename.split(' ')
        # insert 0th element from namelist back into row as 1st element
        # then 1st element of namelist back into row as 2nd element
        for i in range(1, 3):
            row.insert((i), namelist[i-1])
    # return modified array
    return rawarray

# execute above fix to array and return
arrayfix1 = splitname()

# splitdate() extracts yyyy-mm-dd date from list, converts to yyyy/mm/dd
# and inserts it back into the original list
def splitdate():
    # iterate over rows in array
    for row in arrayfix1:
        # remove and return 3rd element from row (date)
        wholedate = row.pop(3)
        # split string on '-' delimiter
        datelist = wholedate.split('-')
        # initialize empty list
        newdatelist = []
        # append each element from the split to the empty list
        newdatelist.append(datelist[2])
        newdatelist.append(datelist[1])
        newdatelist.append(datelist[0])
        # join all elements of the new list into string, delimited by '/'
        datestring = '/'.join(newdatelist)
        # insert parsed and transformed string back into row as 3rd element
        row.insert(3, datestring)
    # return the modified array
    return arrayfix1

# execute 2nd fix to array and return
arrayfix2 = splitdate()

# hidessn() replaces all but last 4 digits of SSN with '*' to hide
def hidessn():
    # iterate over rows in array
    for row in arrayfix2:
        # remove and return 4th element from row
        ssn = row.pop(4)
        # split string into list on '-' delimiter
        ssnlist = ssn.split('-')
        # create empty list to hold new hidden SSN pieces
        newssnlist = []
        # append asterisks to represent hidden numbers in SSN to empty list
        newssnlist.append('***')
        newssnlist.append('**')
        # append true last four digits (2nd element of ssnlist) of SSN
        newssnlist.append(ssnlist[2])
        # join list elements into continuous string
        newssnstring = '-'.join(newssnlist)
        # insert parsed and modified string back into row as element 4
        row.insert(4, newssnstring)
    # return the modified array
    return arrayfix2

# execute third fix and return modified array
arrayfix3 = hidessn()

# convstate() converts full state names to state abbreviations
def convstate():
    # iterate over rows in array
    for row in arrayfix3:
        # remove and return 5th element of row
        rawstate = row.pop(5)
        # iterate over state abbreviation dictionary to find match
        for key, value in us_state_abbrev.items():
            # if current row's state is found in dictionary, return abbv.
            if key == rawstate:
                shortstate = value
            else:
                pass
        # insert state abbreviation as 5th element of row
        row.insert(5, shortstate)
    # return modified array
    return arrayfix3

# execute 4th fix and return modified array
arrayfix4 = convstate()

# store new header names in list for file writing
header = ['Emp ID', 'First Name', 'Last Name', 'DOB', 'SSN', 'State']
# identify location and name for file to be written
outputpath = os.path.join('output_data', 'fixedemployees.txt')

# open empty file to write
with open(outputpath, 'w', newline='') as f:
    # construct writer object
    writer = csv.writer(f, delimiter=',')
    # write header row first
    writer.writerow(header)
    # then iterate through rows in modified array, writing each to file
    for row in arrayfix4:
        writer.writerow(row)