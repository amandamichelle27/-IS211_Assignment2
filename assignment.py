#!/usr/bin/python
from argparse import ArgumentParser
from datetime import datetime
from logging  import basicConfig, ERROR, getLogger
from sys import exit
from urllib2 import URLError, urlopen

logger = getLogger("assignment2")


def downloadData(url):
    return urlopen(url).read()


def processData(data):
    result = {}
    for index, line in list(enumerate(data.split("\n")))[1:-1]:
        id, name, birthday = line.split(",")
        try:
            birthday = datetime.strptime(birthday, '%d/%m/%Y').date()
            result[int(id)] = (name, birthday)
        except ValueError:
            logger.error("Error processing line #%d for ID #%s", index, id)
    return result


def displayPerson(id, personData):
    try:
        name, birthday = personData[id]
        print "Person #%d is %s with a birthday of %s" % (
            id, name, birthday.strftime("%Y-%m-%d"))
    except KeyError:
        print "No user found with that id"


if __name__ == "__main__":
    # Parse the --url argument.
    parser = ArgumentParser()
    parser.add_argument("--url", required=True)
    url = parser.parse_args().url
    
    # Read in the data from the URL.
    try:
        csvData = downloadData(url)
    except URLError:
        print "Could not fetch data from the given URL:", url
        exit()
    except ValueError:
        print "Invalid URL given:", url
        exit()
    
    # Configure the logger.
    basicConfig(filename="errors.log", level=ERROR)
    
    # Parse the data.
    personData = processData(csvData)
    
    # Interactively process user input.
    while True:
        try:
            id = int(raw_input("Enter in an ID: "))
        except ValueError:
            print "ID given must be an integer."
            continue
        if id <= 0:
            exit()
        displayPerson(id, personData);
    