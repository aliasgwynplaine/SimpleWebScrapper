# -*- coding: utf-8 -*-
import sys
import requests
import csv
from bs4 import BeautifulSoup

def csvfile2dict(filepath): # Maybe useless, perhabs...
    """takes the path of the file as a string object.
    Returns a dict."""
    with open(filepath, 'r') as csv_file_handler:
        csv_handler = csv.reader(csv_file_handler)
        first_elem = csv_handler.__next__()
        old = first_elem[0]
        if len(first_elem) == 2 :
            mydict = dict({old : [first_elem[1]]})
        else :
            mydict = dict({old : []})

        for i in csv_handler:
            if i != [] :
                if i[0] == old :
                    if len(i) == 2 :
                        mydict[i[0]].append(i[1])

                else :
                    old = i[0]
                    mydict[i[0]] = [i[1]]
            else :
                pass

    return mydict

def google_search(query, startParam) :
    """Takes a query and the start parameter for the google search.
    Makes an HTTP request using GET method to the google news section
    and saves 10 new's url, at most, in a set object that is returned.
    If no data is found, returns None"""

    target_url = 'https://www.google.com/search?tbm=nws&q={}&start={}'
    target_url = target_url.format(query.replace(' ', '+'), startParam)

    headers = {
        'User-Agent': 'Mozilla/5.0 Firefox/69.0', # important. HTMLdoc depends on useragent
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
        'Host': 'www.google.com'
    }

    response = requests.get(target_url, headers=headers)

    if response.status_code == 200 :
        soup = BeautifulSoup(response.content, 'html.parser')
        hrefs = soup.select('.r a') # selecting all href elements

        if hrefs == [] :
            sys.stdout.write("No results for {} at startpoint {} were found\n".format(query, startParam))
            return []

        aux_get_fux = lambda x : x.get('href') # to call get fuction of hrefs

        listofnews = map(aux_get_fux, hrefs) # this is faster than a for loop

        return list(listofnews)


    else :
        sys.stderr.write("Something bad happened! ")
        sys.stderr.write("Response status code: {}\n".format(response.status_code))
        return []



if __name__ == "__main__":
    query = '1328749182 3918ueif10487r1y02873rg|2u3he098h|\'2938h|087423r'
    pass
