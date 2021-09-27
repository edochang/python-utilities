    #!/usr/bin/env python3
import argparse
import os
import sys

# Borrowed utility from https://gist.github.com/jrivero/1085501
def split(filehandler, delimiter=',', row_limit=10000, 
    output_name_template='output_%s.csv', output_path='.', keep_headers=True):
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
    print('field_size_limit: ', sys.maxsize)
    
    maxInt = sys.maxsize

    while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
        try:
            print('maxint: ', maxInt)
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)
    
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
         output_path,
         output_name_template  % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w', newline='', encoding='utf-8'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = next(reader)
        current_out_writer.writerow(headers)
    try:
        for i, row in enumerate(reader):
            if i + 1 > current_limit:
                current_piece += 1
                current_limit = row_limit * current_piece
                print('i: ', i)
                print('current_limit:', current_limit)
                current_out_path = os.path.join(
                output_path,
                output_name_template  % current_piece
                )
                current_out_writer = csv.writer(open(current_out_path, 'w', newline='', encoding='utf-8'), delimiter=delimiter)
                if keep_headers:
                    current_out_writer.writerow(headers)
            current_out_writer.writerow(row)
    except csv.Error as e:
        print('e: ', e)
        sys.exit('line {}: {}'.format(reader.line_num, e))

parser = argparse.ArgumentParser(prog="FileSplitter", description='A script that splits a file that contains rows of records separated with a line feed.')
parser.add_argument('-file', help='fullpath of the file to be split')
parser.add_argument('-chunksize', help='size of each chunked file')
args = parser.parse_args()

strSourceFullFilePath = args.file

# Get working directory
strWorkingDirectory = strSourceFullFilePath[0:strSourceFullFilePath.rfind('\\')+1]
strSourceFileName = strSourceFullFilePath[strSourceFullFilePath.rfind('\\')+1:len(strSourceFullFilePath)-4]
strTargetFileExtension = '.csv'
print('Working directory containing source file: ', strWorkingDirectory)
print('Source filename: ', strSourceFileName)

# open csv file using 'with'.  The with statement simplifies exception handling by encapsulating 
# common preparation and cleanup tasks.  In addition, it will automatically close the file. 
# The with statement provides a way for ensuring that a clean-up is always used
with open(strSourceFullFilePath, 'r', encoding='utf-8', errors='replace') as file:
    for count, line in enumerate(file):
        pass

# Get final count of records in the file
intFileRecordCount = count + 1
print('Total record count: ', intFileRecordCount)

'''
# Determine the chunk file count
decChunkCount = intFileRecordCount / 3
print('Chunk group count: ', decChunkCount)
'''
# If chunksize is not defined, then default it to 10,000 records.
try:
    decChunkCount = int(args.chunksize)
except:
    decChunkCount = 10000

strTargetFileNameTemplate = strSourceFileName + '(%s)' + strTargetFileExtension

# Re-open csv file to chunk the files
filedata = open(strSourceFullFilePath, 'r', encoding='utf-8', errors='replace')


split(filedata, delimiter='|', row_limit=decChunkCount,output_name_template=strTargetFileNameTemplate, output_path=strWorkingDirectory)

'''
try:    
    split(open(strSourceFullFilePath, 'r'),delimiter='\t', row_limit=decChunkCount,output_name_template=strTargetFileNameTemplate, output_path=strWorkingDirectory)
except Exception as e:
    print(e)
'''
