#!/usr/bin/env python3
# n262ynab.py
# create YNAB CSV import file based on N26 CSV export

import sys
import csv
import decimal


def fmtDate(sdate):
    return sdate[5:7] + '/' + sdate[8:11] + '/' + sdate[2:4]

def n262ynab(inFile, outFile):
    reader = csv.reader(open(inFile), delimiter=",")
    writer = csv.writer(open(outFile, "w", newline=''), delimiter=",") 

    writer.writerow(["Date", "Payee", "Memo", "Outflow", "Inflow"])

    rowidx = 0
    for row in reader:
        rowidx = rowidx + 1

        #skip header
        if rowidx == 1:
            continue

        print(row[0] + " " + row[1] + " " + row[6])

        amount = decimal.Decimal(row[6])

        #skip info lines
        if amount == 0:
            continue

        if amount < 0:
            writer.writerow([fmtDate(row[0]), "", row[1], str(amount * -1), ""])
        else:
            writer.writerow([fmtDate(row[0]), "", row[1], "", str(amount)])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s infile (outfile)" % sys.argv[0])
    else:
        # create name for output file if it is not given
        if len(sys.argv) == 2:
            outFile =  "./" + sys.argv[1].split(".")[1] + "_YNAB.csv"
        else:
            outFile = "./" + sys.argv[2]

        n262ynab(sys.argv[1], outFile)
        print("%s --> %s" % (sys.argv[1], outFile))  