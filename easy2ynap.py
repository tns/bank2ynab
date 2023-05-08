#!/usr/bin/env python3
# easy2ynab.py
# create YNAB CSV import file based on easybank CSV export

import sys
import csv
import decimal


def fmtDate(sdate):
    return sdate[5:7] + '/' + sdate[8:11] + '/' + sdate[2:4]

def easy2ynab(inFile, outFile):
    reader = csv.reader(open(inFile), delimiter=";")
    writer = csv.writer(open(outFile, "w", newline=''), delimiter=",") 

    writer.writerow(["Date", "Payee", "Memo", "Outflow", "Inflow"])

    rowidx = 0
    for row in reader:
        rowidx = rowidx + 1

        #skip header
        #if rowidx == 1:
        #    continue

        #format numbers
        row[4] = row[4].replace(".", "")
        row[4] = row[4].replace(",", ".")
        amount = decimal.Decimal(row[4])

        #skip info lines
        if amount == 0:
            continue

        if amount < 0:
            writer.writerow([row[3], "", row[1], str(amount * -1), ""])
        else:
            writer.writerow([row[3], "", row[1], "", str(amount)])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s infile (outfile)" % sys.argv[0])
    else:
        # create name for output file if it is not given
        if len(sys.argv) == 2:
            outFile =  "./" + sys.argv[1].split(".")[1] + "_YNAB.csv"
        else:
            outFile = "./" + sys.argv[2]

        easy2ynab(sys.argv[1], outFile)
        print("%s --> %s" % (sys.argv[1], outFile))  
