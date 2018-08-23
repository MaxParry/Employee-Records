import os
import csv

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

sourcedirectory = 'input_data'
file1 = 'employee_data1.csv'
file2 = 'employee_data2.csv'
filelist = [file1, file2]


# for exploration, prints n number of rows in each file

def shown(n):
    for afile in filelist:
        counter = 0
        path = os.path.join(sourcedirectory, afile)
        with open(path, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                counter = counter + 1
                print(row)
                if counter >= n:
                    print('')
                    break

# countvotes() returns total number of votes, skipping headers

def countemps():
    totcount = 0
    for afile in filelist:
        counter = 0
        path = os.path.join(sourcedirectory, afile)
        with open(path, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[0] == 'Emp ID':
                    pass
                else:
                    counter = counter + 1
        totcount = totcount + counter
    return totcount

# unpacks employee data into an array

def unpack():
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

rawarray = unpack()

def splitname():
    for row in rawarray:
        wholename = row.pop(1)
        namelist = wholename.split(' ')
        for i in range(1, 3):
            row.insert((i), namelist[i-1])
    return rawarray

arrayfix1 = splitname()

def splitdate():
    for row in arrayfix1:
        wholedate = row.pop(3)
        datelist = wholedate.split('-')
        newdatelist = []
        newdatelist.append(datelist[2])
        newdatelist.append(datelist[1])
        newdatelist.append(datelist[0])
        datestring = '/'.join(newdatelist)
        row.insert(3, datestring)
    return arrayfix1

arrayfix2 = splitdate()

def hidessn():
    for row in arrayfix2:
        ssn = row.pop(4)
        ssnlist = ssn.split('-')
        newssnlist = []
        newssnlist.append('***')
        newssnlist.append('**')
        newssnlist.append(ssnlist[2])
        newssnstring = '-'.join(newssnlist)
        row.insert(4, newssnstring)
    return arrayfix2

arrayfix3 = hidessn()

def convstate():
    for row in arrayfix3:
        rawstate = row.pop(5)
        for key, value in us_state_abbrev.items():
            if key == rawstate:
                shortstate = value
            else:
                pass
        row.insert(5, shortstate)
    return arrayfix3

arrayfix4 = convstate()

header = ['Emp ID', 'First Name', 'Last Name', 'DOB', 'SSN', 'State']
outputpath = os.path.join('output_data', 'fixedemployees.txt')

with open(outputpath, 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(header)
    for row in arrayfix4:
        writer.writerow(row)