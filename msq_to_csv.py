import csv

inputFileName = input('Enter MSQ filename: ')
numGradeFields = input('Enter the number of grade fields: ')
outputFileName = input('Enter output CSV filename: ')

msqFile = open(inputFileName)
outFile = open(outputFileName, 'wb')

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
    cumTonnes = 'NaN'
    parcelCount = 'NaN'
    headerTonnes = 'NaN'
    period = 'NaN'
    fraction = 'NaN'
    pushback = 'NaN'
    parcels = 'NaN'
    cumTonnes = 'NaN'
    parcelCount = 'NaN'
    headerFlag = 'NaN'
    
    for row in reader:
        print row
        try:
            #Index 3 should be parcels (int) in a header line, rocktype (str) in parcel line 
            #Try to convert to int...
            parcels = int(row[3])
        except ValueError:
            #...raise ValueError exception if you try to convert string to int - probably a parcel line
            headerFlag = 0
        except IndexError:
            #Header or parcel row should have at least 4 entries, if not, skip row.
            continue
        else:
            headerFlag = 1
                  
        if headerFlag == 1:                               # Check if header row
            headerTonnes = float(row[6])
            period = int(row[7])
            fraction = float(row[8])
            pushback = int(row[9])
            parcels = int(row[3])
            cumTonnes = 0.00                              # Reset cumulative tonnes for this block of parcels
            parcelCount = 0                               # Reset parcel count for this block of parcels
        elif len(row) == (6 + numGradeFields):            # Check if parcel row
            # Read data for parcel row
            rockType = row[3]
            parcelTonnes = float(row[4])
            elementQtys = row[5:(5+numGradeFields)]
            process = row[-1]
            print cumTonnes
            print parcelTonnes
            cumTonnes += parcelTonnes           
            
            # Concatnate header infomation with parcel information
            concRow = [period, fraction, pushback, rockType, parcelTonnes] \
                        + elementQtys + [process] 

            writer.writerow(concRow)
            parcelCount += 1

            if parcelCount == parcels and cumTonnes < headerTonnes:
                missingTonnes = headerTonnes - cumTonnes
                unclass_row = [period, fraction, pushback, 'UNK', 
                                missingTonnes] \
                                + [0.0 for i in range(numGradeFields)] \
                                + ['-np-']
                writer.writerow(unclass_row)
        else:
            print('WARNING - NOT HEADER OR PARCEL ROW: ')
            print(str(row))
            print

finally:
    msqFile.close()
    outFile.close()
    
    print("Program Exited.")
    