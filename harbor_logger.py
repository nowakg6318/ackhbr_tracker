'''Collects data on the current ships in Auckland Harbor.

Uses Beautiful Soup4 to collects and stores data on ships in Auckland
Harbor. This data includes ship names, sizes, flags, and the type of
ship.

Example:
    $ python harbor_logger.py()
'''

from bs4 import BeautifulSoup as bs4
import requests

import csv
import time


def CollectData():
    '''Collects data on the current ships in Auckland Harbor.

    This function collects data on the ships in Auckland Harbor. The data
    is scraped using the requests and beautiful soup4 packages.

    Args:
        None

    Returns:
        list: Returns a 2D list, where each column is a list to be written to
        the csv file.

    Raises:
        None
    '''

    # Grab html from Port of Auckland page.
    harbor_page = requests.get('') # noqa
    soup1 = bs4(harbor_page.content, 'html.parser')
    headers = {'User-Agent': ''} # noqa

    csv_list = []

    #  Grab html from each ship page.
    for ship_tag in soup1.find_all('td', 'name'):
        name = ship_tag.text.strip()
        imo = ship_tag.find_next_sibling(attrs='lloydsNum').text.strip()
        previous_port = (ship_tag.find_next_siblings(attrs='port')[0]
                         .text.strip())

        next_port = ship_tag.find_next_siblings(attrs='port')[1].text.strip()
        dock = (ship_tag.find_next_sibling(attrs='refs').text.strip()
                .split()[0])

        if not int(imo):
            continue

        ship_page = requests.get('' # noqa
                                 + str(imo), headers=headers)

        soup2 = bs4(ship_page.content, 'html.parser')
        ship_type = (soup2.find('a', 'font-120').text.strip())

        flag = (soup2.find('span', string='Flag: ')
                .find_next_sibling('b').text.strip()[:-5])

        gross_tonnage = (soup2.find('span', string='Gross Tonnage: ')
                         .find_next_sibling('b').text.strip())

        deadweight_tonnage = (soup2.find('span', string='Deadweight: ')
                              .find_next_sibling('b').text.strip()[:-2])

        ship_list = [name, imo, ship_type, flag, gross_tonnage,
                     deadweight_tonnage, dock, previous_port, next_port]

        csv_list.append(ship_list)

        #  Sleep for a second.
        time.sleep(1)

    return(csv_list)


def WriteData(data_list, file_name='auckland_harbor_data.csv'):
    '''Appends data to a csv file and adds a time stamp to each row.

    Args:
        data_list (list): A 2D list where each column should be written
        to the given csv file (file_name).

        file_name (string, optional): A string representing the csv file
        name the data should be written to.

    Returns:
        None

    Raises:
        None
    '''

    #  Open File
    file = open(file_name, 'a', newline='')
    writer = csv.writer(file)

    #  Write information to csv file.
    time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    for column in data_list:
        writer.writerow([time_string] + column)

    #  Close File
    file.close()


if __name__ == '__main__':
    data = CollectData()
    WriteData(data)
