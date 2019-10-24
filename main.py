# -*- coding: utf-8 -*-

import sys
import pandas
import requests
from time import time
from functools import reduce
from swsutils import *

if __name__ == "__main__":
    if len(sys.argv) == 4 :
        inputfilepath = sys.argv[1]
        outputfilepath = sys.argv[2]
        MAX_NUMBER_OF_PAGES = int(sys.argv[3])

        start = time()
        sys.stdout.write("Running...\n")

        target_info = csvfile2dict(inputfilepath)
        listofkeywords = list()
        total_links = list()

        for field in target_info.keys() :
            if target_info[field] == [''] :
                total_links += ['No queries']
                listofkeywords += [field + ' no queries']
            else :
                for keywords in target_info[field] :
                    for startpoint in range(MAX_NUMBER_OF_PAGES):
                        tmp_list = google_search(keywords, startpoint * 10 + 1)
                        total_links += tmp_list
                        listofkeywords += [field + ' ' + keywords] * len(tmp_list)

        df = pandas.DataFrame({'url': total_links, 'keywords': listofkeywords})
        df.to_excel(outputfilepath, index=True, encoding='utf-8')
        sys.stdout.write("Completed!\n")
        sys.stdout.write("Time: {}\n".format(time() - start))

        exit(0)
    else :
        sys.stderr.write(
            "Usage: python3 {} <inputfile> <outputfile> <max_number_of_pages>\n".format(sys.argv[0])
        )
        exit(1)
