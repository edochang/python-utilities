#!/usr/bin/env python3
import argparse
from CSVOps import *
from Validator import *

# Global class variables
OPERATIONS = ['chunk']

def main():
    ''' Main logic for the CTI script.
    '''
    # Example Call: python ./FileSplitter.py --file <File_Full_Path>
    parser = argparse.ArgumentParser(prog="CTI", description='CTI, CSV Terminal Interface, is a script that manipulates / operates on a csv file.')
    parser.add_argument('-operation', help='Select the operation you want to do.  Valid operations are: ' + str(OPERATIONS))
    parser.add_argument('-file', help='Fullpath of the file to be worked on.')
    parser.add_argument('-chunksize', help='Size of each chunked file.')
    parser.add_argument('-encoding', help='Define the encoding of the file.  If nothing is defined then the script will default to utf-8.')
    parser.add_argument('-delimiter', help='Delimiter used for the csv file')
    args = parser.parse_args()

    # Validate terminal arguments
    strOperation, strSourceFullFilePath, intChunkSize, strEncoding, strDelimiter = validateArgs(args)

    # Read CSV File
    csv = CSVOps(strSourceFullFilePath, strEncoding, strDelimiter)

    # Get final count of records in the file
    intRecordCount = csv.getCSVLength()
    print('[INFO] Total CSV Record Count: ', intRecordCount)

    if strOperation == 'chunk':
        chunk(csv, intChunkSize, strEncoding, strDelimiter)

def chunk(csv, chunk_size, encoding, delimiter):
    '''
    Args:
        csv (CSVData):  Instance of CSVOps to operate on the CSV file and its data.
        chunk_size (Integer):  The size of each chunk / batch CSV file to be written.
        encoding (String):  Note: Python's default encoding is ASCII.  This parameter forces default encoding for the writer to be utf-8.
        delimiter (String):  Defines the delimiter used to separate the data columns within a CSV record.
    '''
    print('[INFO] Begin CSV Chunking...')
    csv.writeFileChunk(chunk_size=chunk_size, encoding=encoding, delimiter=delimiter)
    print('[INFO] CSV chunking is done.')

def validateArgs(input):
    ''' Validate if the arguments have been defined or not.
    Args:
        input (Namespace):  A Namespace object containing attributes parsed out of the command line.  See Python Documentation for more details: https://docs.python.org/3/library/argparse.html?highlight=parse_args#argparse.ArgumentParser.parse_args
    Returns:
        operation (String):  The operation that the user wants to do.
        file (String):  Fullpath of the file.
        chunksize (Integer):  Size of each chunked file.
        encoding (String):  Define the encoding of the file.  If nothing is defined then the script will default to utf-8.
        delimiter (String):  Delimiter used for the csv file.  If nothing is defined then the script will default to ','.
    '''
    operation = input.operation
    file = input.file
    chunksize = input.chunksize
    encoding = input.encoding
    delimiter = input.delimiter

    if stringBlankOrNone(operation):
        print('[ERROR] The -operation argument cannot be blank.  When calling this script, add --help / -h for more details.')
        print('[WARNING] Script is exiting...')
        quit()
    else:
        if (str.lower(operation) not in OPERATIONS):
            print('[ERROR] The -operation argument is not valid.  It needs to be at least one of these values: ' + str(OPERATIONS))
            print('[WARNING] Script is exiting...')
            quit()

    if stringBlankOrNone(file):
        print('[ERROR] The -file argument cannot be blank.  When calling this script, add --help / -h for more details.')
        print('[WARNING] Script is exiting...')
        quit()
    
    if operation == 'chunk':
        if not isInt(chunksize):
            print('[ERROR] The -chunksize argument must be an integer.  When calling this script, add --help / -h for more details.')
            print('[WARNING] Script is exiting...')
            quit()
        else:
            chunksize = 5000
            print('[INFO] No chunksize argument.  Default chunksize used: ', chunksize)

    if stringBlankOrNone(encoding):
        encoding = 'utf-8'
        print('[INFO] No encoding argument.  Default Encoding used: ', encoding)
    
    if stringBlankOrNone(delimiter):
        delimiter = ','
        print('[INFO] No delimiter argument.  Default delimiter used: ', delimiter)
    
    return operation, file, chunksize, encoding, delimiter

if __name__ == "__main__":
    main()