# <a name='python-utilities'>python-utilities</a>
A repository of useful python utilities.
1. [CSV Operations Terminal Interface (COTI)](#coti)
2. [Prototypes](#prototypes)


Python Version Notes:  These scripts was written with Python 3.9.7.

# <a name='coti'>1. CSV Operations Terminal Interface (COTI)</a>
A python script used to read in a CSV, store the data in-memory, and apply a series of operations to it.

Supported operations:
|Operations|Description|
|----------|-----------|
|chunk|Takes a CSV file and chunks the records into multiple files.|

## General Instructions
To use the this script, navigate to the directory that contains the COTI.py file and call the following command for additional instructions.

    python ./COTI.py --h

This will explain to you how the scripts work and what arguments you can add to this script call.

## Chunk Operation Instructions
Call Example:

    python ./COTI.py -file="C:\Users\username\working_directory\file name.csv" -operation='chunk' -chunksize=5000

## References
The creation of COTI was inspired from https://gist.github.com/jrivero/1085501.  The general logic was inspired from here, however COTI was designed to be extendable for additional CSV manipulation operations.

# <a name='prototyeps'>2. Prototypes</a>
Random scripts that was written on the fly to achieve specific tasks.  These functions have not been incorporated to the overall utilities listed in [python-utilites](#python-utilites).