#########
# Date Created: 02/19/2018
# Created By: Pankhuri Kumar (pk2569)
#
# The data used here is taken from NYC Open Data's 311 Complaints Dataset, filtered for Water-related complaints:
#   https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
#
# This file reads in a CSV file storing water-related complaints in NYC and plots a histogram with lines for
#   measures of central tendency according to the time taken to respond to the plumbing complaints.
#
# The flow of the program:
#       1. read in the file and create a DictReader for it
#       2. read the created and closed time for each complaint related to plumbing
#       3. convert this time to Unix timestamp and subtract to find the seconds between creation and closing
#       4. store the number of days taken by the DOB/HPD to respond
#       5. calculate the median- and mean-related values and print them
#       6. plot the histogram, and median-, mean-related lines
#
# The histogram shows that there are certain response times that lie beyond the second sigma line,
#   which is an extraordinary amount of time to be responding to these requests (> 1000 days). It would be worth
#   exploring what these complaints were about, or which borough/community board/zipcode they occur in and if
#   any pattern emerges.
#########

#to read data
import csv
# for calculations on the data
import numpy as np
import matplotlib.pyplot as plotlib
import statistics
# for conversion of time to Unix timestamp
from datetime import datetime
import time

# Opening my csv and creating a DictReader
myFile = open("311complaints_Plumbing.csv", 'rU')
newFile = open("Plumbing_AB.csv", 'w')
plumbingData = csv.DictReader(myFile)
abnormalPlumbing = csv.DictWriter(newFile, fieldnames=plumbingData.fieldnames)
abnormalPlumbing.writeheader()

# creating a new data set of just the plumbing complaints, to prevent excess memory usage
# row_names are "complaint_type", "created_date" and "closed_date"
responseTime = []
for row in plumbingData:
    # some of the plumbing complaints are still open, so there is no closed date
    # hence putting in a try-except statement
    try:
        # convert API's datetime representation to datetime, and then Unix timestamp
        # and then subtract to get time to response
        if (row['complaint_type'] == 'Plumbing' or row['complaint_type'] == 'PLUMBING'):
            # specifying the date format used in the data
            format = '%Y-%m-%dT%H:%M:%S.%f'
            # converting the data into Unix timestamp
            createdDate = time.mktime(datetime.strptime(row['created_date'], format).timetuple())
            closedDate = time.mktime(datetime.strptime(row['closed_date'], format).timetuple())
            # storing response time in days -- any lower unit is too large for graphs
            rT = int(closedDate - createdDate) / (60*60*24)
            responseTime.append(rT)
            if (rT > 1000):
                abnormalPlumbing.writerow(row)
    except:
        pass

# measures of central tendencies below
# quartiles, upper and lower bounds
quartileLines = np.percentile(responseTime, [25, 50, 75])
interQuartile = quartileLines[2] - quartileLines[0]
upperBoundLine = quartileLines[2] + 1.5*interQuartile
lowerBoundLine = quartileLines[2] - 1.5*interQuartile

# mean, standard deviation, and sigma intervals
mean = statistics.mean(responseTime)
stdDev = np.std(responseTime)
meanLines = [mean]
for i in range(1, 4):
    meanLines.append(mean + i*stdDev)
    meanLines.append(mean - i*stdDev)

# printing all the data
print("The different lines drawn on the histogram are: ")
print("\t(black) The median response time to plumbing complaints is " + str(quartileLines[1]) + " days.")
print("\t(black) The 25th and 75th quartiles for the data are " + str(quartileLines[0]) + " and " + str(quartileLines[2]) + " days respectively.")
print("\t(red) The mean response time to plumbing complaints is " + str(mean) + " days.")
print("\t(red) The first std deviation from the mean is (" + str(meanLines[2]) + ", " + str(meanLines[1]) + ")")
print("\t(red) The second std deviation from the mean is (" + str(meanLines[4]) + ", " + str(meanLines[3]) + ")")
print("\t(red) The third std deviation from the mean is (" + str(meanLines[6]) + ", " + str(meanLines[5]) + ")")
print("\tThe standard deviation for the data is " + str(stdDev))


# building a histogram of the data
zipHistogram = plotlib.hist(responseTime, bins = 50, histtype='bar', color=['green'])

# displaying the plots
# quartileLines, upper and lower bounds in black
plotlib.vlines(quartileLines, 0, 900, color=['k', 'k', 'k'], linestyles='dashed', linewidth = 1.5)
plotlib.vlines([lowerBoundLine, upperBoundLine], 0, 900, color=['k', 'k'], linestyles='dashed', linewidth = 1.5)
# mean and sigma lines in red
plotlib.vlines(meanLines, 0, 900, color=['r'], linestyles='dashed', linewidth = 1.5)
plotlib.show()