#!/usr/bin/env python3
class CSVData (object):
    # Class Attributes
    hasData = None
    dataHeader = None
    data = None

    def __init__(self):
        ''' Class instantiation method
        '''
        self.hasData = False
        self.dataHeader = []
        self.data = []