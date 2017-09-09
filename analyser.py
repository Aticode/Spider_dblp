# -*- coding: utf-8 -*-
import os
import sys
import re
import csv

searchkey = 'homomorphic'.lower()

def main():
    fileDir = os.path.split(os.path.realpath(sys.argv[0]))[0] + os.sep + 'source'
    for root, dirs, files in os.walk(fileDir):
        for file in files:
            filename = os.path.join(root, file)
            with open(filename,'r',encoding='utf-8',newline='') as source:
                reader = csv.reader(source)
                for row in reader:
                    area = row[2].lower()
                    title = row[3].lower()
                    if (searchkey in area) or (searchkey in title):
                        resultrow = (row[0], row[1], row[2], row[3], row[4], row[5])
                        with open(searchkey + '.csv','a',encoding='utf-8',newline='') as result:
                            writer = csv.writer(result)
                            writer.writerow(resultrow)
                        result.close()
            source.close()

if __name__ == '__main__':
    main()
