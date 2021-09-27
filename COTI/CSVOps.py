#!/usr/bin/env python3
import csv
import os
from CSVData import *
'''
CSVReader is a functon script that enables other scripts to read CSVs.
'''

class CSVOps(object):
     # Private Class Attributes
     __working_directory = ''
     __source_file_name = ''
     __source_file_extension = ''
     __output_filename_template = ''
     __current_output_writer = None
     __data_csv = None

     def __init__(self):
          ''' Class instantiation method
          '''
          self.__delimiter = ','  # default delimiter to comma (,)
          self.instantiateDataCSV()

     def __init__(self, source_file_path, encoding='utf-8', delimiter=','):
          ''' Class instantiation method with parameters
          Args:
               source_file_path (String):  Contains the full file path and file name of the source file (e.g. C:\directory\filepath\file.csv).
               encoding (String):  Defines the encoding which the source file should be read.  By code, defaults to utf-8.
               delimiter (String):  Defines the delimiter used to separate the data columns within a CSV record.
          '''
          self.instantiateDataCSV()
          self.readFile(source_file_path, encoding, delimiter)
     
     def instantiateDataCSV(self):
          ''' Instantiates the CSVData object to store the data from the CSV file.
          '''
          self.__data_csv = CSVData()

     def readFile(self, source_file_path, encoding='utf-8', delimiter=','):
          ''' Reads a csv file and converts each line and its field into an array where the element of the arrays contains the column data for each CSV record.
          Args:
               source_file_path (String):  Contains the full file path and file name of the source file (e.g. C:\directory\filepath\file.csv).
               encoding (String):  Defines the encoding which the source file should be read.  By code, defaults to utf-8.
               delimiter (String):  Defines the delimiter used to separate the data columns within a CSV record.
          '''
          # Get working directory
          self.__working_directory = source_file_path[0:source_file_path.rfind('\\')+1]
          self.__source_file_name = source_file_path[source_file_path.rfind('\\')+1:len(source_file_path)-4]
          self.__source_file_extension = source_file_path[len(source_file_path)-4:len(source_file_path)]
          print('[INFO] Working directory containing source file: ', self.__working_directory)
          print('[INFO] Source filename and extension: ', self.__source_file_name + self.__source_file_extension)
          self.__output_filename_template = self.__source_file_name + '(%s)' + self.__source_file_extension

          # Open csv file using 'with'.  The with statement simplifies exception handling by encapsulating common preparation and cleanup tasks.  In addition, it will automatically close the file.  The with statement provides a way for ensuring that a clean-up is always used
          with open(source_file_path, 'r', encoding=encoding) as filehandler:
               reader = csv.reader(filehandler, delimiter=delimiter)
               self.__data_csv.dataHeader = next(reader)
          
               for i, row in enumerate(reader):
                    self.__data_csv.data.append(row)

               if len(self.__data_csv.data) != 0:
                    self.__data_csv.hasData = True

     def getCSVData(self):
          ''' Returns the CSVData object.
          Returns:
               (CSVData):  Object containing the csv data that was read from readFile().
          '''
          return self.__data_csv
     
     def getCSVLength(self):
          ''' Returns the number of records in the CSV file.
          Returns:
               (Integer):  The number of records in CSVData.data that was read from readFile().
          '''
          return len(self.__data_csv.data)

     def setWriter(self, encoding, delimiter, current_piece, newline=''):
          ''' Sets a new CSV writer to output a new CSV file.
          Args:
               encoding (String):  Note: Python's default encoding is ASCII.  This parameter forces default encoding for the writer to be utf-8.
               delimiter (String):  Defines the delimiter used to separate the data columns within a CSV record.
               current_piece (String):  Defines different parts / batches of the same output file.  (e.g. Filename (1), Filename (2)...)
               newline (String):  Controls how universal newlines mode works. It can be None , '' , '\n' , '\r' , and '\r\n'.  

          Notes:
               newline:  When writing output to the stream, if newline is None , any '\n' characters written are translated to the system default line separator, os.linesep. If newline is '' or '\n' , no translation takes place. If newline is any of the other legal values, any '\n' characters written are translated to the given string.
          '''
          current_output_path = os.path.join(
               self.__working_directory, 
               self.__output_filename_template % current_piece
          )
          self.__current_output_writer = csv.writer(open(current_output_path, 'w', encoding=encoding, newline=newline), delimiter=delimiter)

     def writeFileChunk(self, chunk_size, keep_header=True, encoding='utf-8', delimiter=','):
          '''
          Args:
               chunk_size (Integer):  The size of each chunk / batch CSV file to be written.
               keep_header (Boolean):  Defines whether the headers should be kept or not in the CSV file.
               encoding (String):  Note: Python's default encoding is ASCII.  This parameter forces default encoding for the writer to be utf-8.
               delimiter (String):  Defines the delimiter used to separate the data columns within a CSV record.
          '''
          intCurrentPiece = 1
          intCurrentLimit = chunk_size

          self.setWriter(encoding, delimiter, intCurrentPiece)

          if keep_header:
               self.__current_output_writer.writerow(self.__data_csv.dataHeader)

          for i, row in enumerate(self.__data_csv.data):
               if i + 1 > intCurrentLimit:
                    print('[INFO] Finish writing chunk ' + str(intCurrentPiece) + '.')
                    intCurrentPiece += 1
                    intCurrentLimit = chunk_size * intCurrentPiece
                    self.setWriter(encoding, delimiter, intCurrentPiece)
                    if keep_header:
                         self.__current_output_writer.writerow(self.__data_csv.dataHeader)
               self.__current_output_writer.writerow(row)
          print('[INFO] Finish writing chunk ' + str(intCurrentPiece) + '.')