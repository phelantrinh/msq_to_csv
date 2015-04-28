import csv

def readParElements(inputFileName):
    '''Read the elements from a Whittle parameters file
    
    Args:
        inputFileName (str): Filename of the parameters file to be parsed
    Returns:
        dict: Dictionary of elements found with order number as the key
    '''
    
    #Open the parameters file
    
    
    try:
        parFile = open(inputFileName)
        
    except:
        print 'Error opening parameters file.'
        
    else:
        reader = csv.reader(parFile)
        
        elementDict = {}

        for row in reader:
            currentRow = row[0]
            #Line type is first 3 columns for file. See Whittle readme.
            lineType = int(currentRow[:3])
            if lineType == 18: #Line type 18 is an element description line
                element = currentRow[4:9].strip()
                modelPosition = int(currentRow[10:25])
                elementDict[modelPosition] = element
        
    finally:
        # Close the file
        parFile.close()
        
        return elementDict
    