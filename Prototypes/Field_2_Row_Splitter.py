#!/usr/bin/env python3
import argparse
import os

# Borrowed utility from https://gist.github.com/jrivero/1085501
def split(filehandler, delimiter=',', output_name_template='output_%s.csv', output_path='.', keep_headers=True, input_encoding='UTF-8', field_2_split=0, field_delimiter=';' ,split_field_only='yes'):
    """
    Splits a CSV file into multiple pieces.
    
    A quick bastardization of the Python CSV library.
    Arguments:
        `row_limit`: The number of rows you want in each output file. 10,000 by default.
        `output_name_template`: A %s-style template for the numbered output files.
        `output_path`: Where to stick the output files.
        `keep_headers`: Whether or not to print the headers in each output file.
    Example usage:
    
        >> from toolbox import csv_splitter;
        >> csv_splitter.split(open('/home/ben/input.csv', 'r'));
    
    """
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
         output_path,
         output_name_template  % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w', encoding=input_encoding, newline=''), delimiter=delimiter)
    if keep_headers:
        headers = next(reader)
        current_out_writer.writerow(headers)
    counterSplit=0
    counterNotSplit=0
    for i, row in enumerate(reader):
        if isFieldSplit(row, field_2_split, field_delimiter):
            counterSplit+=1
            field2RowSplitter(current_out_writer, row, field_2_split, field_delimiter)
        else:
            if split_field_only == "no":
                counterNotSplit+=1
                current_out_writer.writerow(row)
    print('[INFO] Number of Rows Identified for Split: ', counterSplit)
    print('[INFO] Number of Rows Identified not for Split: ', counterNotSplit)

def isFieldSplit(input_row, field_2_split, field_delimiter):
    if field_delimiter in input_row[field_2_split]:
        return True
    else:
        return False

def field2RowSplitter(current_out_writer, input_row, field_2_split, field_delimiter):
    itemList = input_row[field_2_split].split()
    for item in itemList:
        output_row = input_row
        output_row[field_2_split] = item
        current_out_writer.writerow(output_row)

def updateDocumentNo(input):
    documentNumber = input[3]
    installmentId = input[15]
    updatedDocumentNumber = documentNumber + '-' + installmentId
    input[3] = updatedDocumentNumber
    
    return input

parser = argparse.ArgumentParser(prog="Field_2_Row_Splitter", description='A script that splits an column list value into additional rows while keeping the remaining columns the same value.')
parser.add_argument('-file', help='Fullpath of the input file')
parser.add_argument('-delimiter', help='Delimiter used for the csv file')
parser.add_argument('-field2split', help='Field to split the list values into additional rows.  Value should be provided using a 0 number counting system (e.g. column1 = 0, column2 = 1, etc.)')
parser.add_argument('-fielddelimiter', help='The delimiter to split the field into additional rows.  Must be encapsulated with quotes.')
parser.add_argument('-encoding', help='Input file encoding (e.g. "UTF-8")')
parser.add_argument('-splitfieldonly', help='Specify if the output file should only contain the field split rows - "yes" or "no"')
args = parser.parse_args()

strSourceFullFilePath = args.file

# Get working directory
strWorkingDirectory = strSourceFullFilePath[0:strSourceFullFilePath.rfind('\\')+1]
strSourceFileName = strSourceFullFilePath[strSourceFullFilePath.rfind('\\')+1:len(strSourceFullFilePath)-4]
strTargetFileExtension = '.csv'
print('[INFO] Working directory containing source file: ', strWorkingDirectory)
print('[INFO] Source filename: ', strSourceFileName)

# If delimiter is not defined, then default it to UTF-8.
if args.delimiter != None:
    strDelimiter = args.delimiter
    print('[INFO] Delimiter used: ', strDelimiter)
else:
    strDelimiter = ","
    print('[INFO] Default Delimiter used: ', strDelimiter)

# If encoding is not defined, then default it to UTF-8.
if args.encoding != None:
    strEncoding = args.encoding
    print('[INFO] Encoding used: ', strEncoding)
else:
    strEncoding = "UTF-8"
    print('[INFO] Default Encoding used: ', strEncoding)

# If field2split and fielddelimiter is not defined, exit the script.
if args.field2split == None or args.fielddelimiter == None:
    print("[WARNING] field2split parameter or fielddelimiter is not defined.  The script will quit...")
    quit()
else:
    try:
        intField2Split = int(args.field2split)
    except ValueError as err:
        print('[WARNING] field2split must be an integer value.  The script will quit...')
        print('[WARNING] Value Error Message: ', err)
        quit()

    strFieldDelimiter = args.fielddelimiter
    print('[INFO] field2split: ', intField2Split)
    print('[INFO] fielddelimiter: ', strFieldDelimiter)

# If splitfieldonly is not defined then default to yes
if args.splitfieldonly != None:
    strSplitFieldOnly = args.splitfieldonly.lower()
    if strSplitFieldOnly == "yes" or strSplitFieldOnly == 'no':
        print('[INFO] SplitFieldOnly: ', strSplitFieldOnly)
    else:
        print('[INFO] SplitFieldOnly: ' + strSplitFieldOnly + ' ; This is not a valid input.  Default value of "yes" will be used.')
        strSplitFieldOnly = "yes"
else:
    strSplitFieldOnly = "yes"
    print('[INFO] Default SplitFieldOnly used: ', strSplitFieldOnly)

'''
open csv file using 'with'.  The with statement simplifies exception handling by encapsulating 
common preparation and cleanup tasks.  In addition, it will automatically close the file. 
The with statement provides a way for ensuring that a clean-up is always used
'''
with open(strSourceFullFilePath, 'r', encoding=strEncoding) as file:
    for count, line in enumerate(file):
        pass

# Get final count of records in the file
intFileRecordCount = count + 1
print('[INFO] Total input record count: ', intFileRecordCount)

strTargetFileNameTemplate = strSourceFileName + '(%s)' + strTargetFileExtension

# Re-open csv file to chunk the files
split(open(strSourceFullFilePath, 'r', encoding=strEncoding),delimiter=strDelimiter,output_name_template=strTargetFileNameTemplate, output_path=strWorkingDirectory, input_encoding=strEncoding, field_2_split=intField2Split, field_delimiter=strFieldDelimiter, split_field_only=strSplitFieldOnly)

'''
try:    
    split(open(strSourceFullFilePath, 'r'),delimiter='\t', row_limit=decChunkCount,output_name_template=strTargetFileNameTemplate, output_path=strWorkingDirectory)
except Exception as e:
    print(e)
'''
