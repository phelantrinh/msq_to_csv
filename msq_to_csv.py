import csv

inputFileName = input('Enter MSQ filename: ')
outputFileName = input('Enter output CSV filename: ')

msqFile = open(inputFileName)
outFile = open(outputFileName, 'wb')

numGradeFields = 8
if numGradeFields > 0:
    parcel_title = []
for i in range(numGradeFields):
    parcel_title += ['qtyElement_'+str(i)]


period = 'NaN'
fraction = 'NaN'
pushback = 'NaN'

titles = ['Period', 'Fraction', 'Pushback', 'RockType', 'Tonnes'] \
            + parcel_title + ['Process']

try:
    reader = csv.reader(msqFile)
    writer = csv.writer(outFile)
    writer.writerow(titles)

except: TypeError
    # Do nothing

else:
    for row in reader:       
        if len(row) == 10:                               # Check if header row
            period = int(row[7])
            fraction = float(row[8])
            pushback = int(row[9])
        elif len(row) == (6 + numGradeFields):           # Check if parcel row
            # Multiply tonnage by fraction to get tonnage for period
            tonnes = fraction * float(row[4])
            
            # Concatnate header infomation with parcel information
            conc_row = [period, fraction, pushback] + [row[3]] + [tonnes] \
                            + row[5:6+(numGradeFields)]
            writer.writerow(conc_row)
        else:
            print('WARNING - NOT HEADER OR PARCEL ROW: ')
            print(str(row))
            print

finally:
    msqFile.close()
    outFile.close()
    
    print("Program Exited.")
    