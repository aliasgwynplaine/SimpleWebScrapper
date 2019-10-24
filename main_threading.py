# -*- coding: utf-8 -*-

import sys
import pandas
import requests
import threading
from time import time
from queue import Queue
from functools import reduce
from swsutils import *

listofkeywords = list()
total_links = list()

if __name__ == "__main__":
    if len(sys.argv) == 5 :
        inputfilepath = sys.argv[1]
        outputfilepath = sys.argv[2]
        NUM_THREADS = int(sys.argv[3])
        MAX_NUMBER_OF_PAGES = int(sys.argv[4])
        task_queue = Queue()

        def worker():
            while True :
                global total_links
                global listofkeywords
                target = task_queue.get()

                if target is None :
                    break

                if target[1] == '' :
                    total_links += ['No queries']
                    listofkeywords += [target[0] + ' no queries']
                else :
                    for startpoint in range(MAX_NUMBER_OF_PAGES):
                        google_search(target[1], startpoint)
                        tmp_list = google_search(target[1], startpoint * 10 + 1)
                        total_links += tmp_list
                        listofkeywords += [target[0] + target[1]] * len(tmp_list)

                task_queue.task_done()


        target_info = csv.reader(open(inputfilepath, 'r'))

        start = time()
        sys.stdout.write("Running using {} threads...\n".format(NUM_THREADS))

        for job in target_info:
            if job != [] :
                task_queue.put(job)

        mythreads = []

        for _ in range(NUM_THREADS):
            t = threading.Thread(target = worker)
            mythreads.append(t)
            t.start()

        task_queue.join()

        for t in range(NUM_THREADS):
            task_queue.put(None)

        map(threading.Thread.join, mythreads)

        df = pandas.DataFrame({'url': total_links, 'keywords': listofkeywords})
        df.to_excel(outputfilepath, index=True, encoding='utf-8')
        sys.stdout.write("Completed!\n")
        sys.stdout.write("Time: {}\n".format(time() - start))

        exit(0)
    else :
        sys.stderr.write(
            "Usage: python3 {} <inputfile> <outputfile> <threads> <max_number_of_pages>\n".format(sys.argv[0])
        )
        exit(1)
