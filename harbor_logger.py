'''Collects data on the current ships in Auckland Harbor.

Uses Beautiful Soup4 to collects and stores data on ships in Auckland
Harbor. This data includes ship names, sizes, flags, and the type of
ship.

Example:
    $ python harbor_logger.py()
'''

import bs4
from bs4 import BeautifulSoup
import requests

import csv
import time
import logging
from logging.handlers import TimedRotatingFileHandler


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

    # Changeable Strings
    harbor_url = ''
    ship_url_base = ''
    headers = {'User-Agent': ''} # noqa

    #  Starting the logger
    logger_format = '%(asctime)s: %(levelname)s: %(message)s'
    logger_handler = TimedRotatingFileHandler('ackhbr.log',
                                              when='H',
                                              interval=1,
                                              backupCount=5)

    logging.basicConfig(format=logger_format, datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.DEBUG,
                        handlers=[logger_handler])

    logger = logging.getLogger(__name__)

    # Grab html from Port of Auckland page.
    logger.info('Connecting to Harbor Page')
    harbor_page = requests.get(harbor_url) # noqa
    ResponseChecker(harbor_page)

    soup1 = BeautifulSoup(harbor_page.content, 'html.parser')

    csv_list = []

    #  Grab html from each ship page.
    for tag in soup1.find_all('tr')[1:]:
        ship_info1 = ([child.text.strip() for child in tag.children
                       if isinstance(child, bs4.element.Tag)])

        logger.debug('Ship data from harbor page: \n {}'
                     .format(ship_info1))

        name = ship_info1[0]
        imo = ship_info1[6]
        previous_port = ship_info1[10]
        next_port = ship_info1[11]
        dock = ship_info1[4].split()[0]

        if int(imo) == 0:
            continue

        ship_page = requests.get(ship_url_base + str(imo), headers=headers)

        ResponseChecker(ship_page)
        soup2 = BeautifulSoup(ship_page.content, 'html.parser')

        ship_type = (soup2.select('a[href*="vessels&ship_type_in"]')[1]
                     .text.strip())

        ship_info2 = ([tag.text.strip() for tag in soup2.find_all('b')
                       if (tag.find_previous_sibling('span')
                           and tag.text.strip())])

        logger.debug('Ship data from ship page: \n {}'
                     .format(ship_info2))

        flag = ship_info2[3][:-5]
        gross_tonnage = ship_info2[5]
        deadweight_tonnage = ship_info2[6][:-2]

        ship_list = ([name, imo, ship_type, flag, gross_tonnage,
                      deadweight_tonnage, dock, previous_port, next_port])

        logger.info('List to be appended to csv file: \n {}'
                    .format(ship_list))

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
    logger = logging.getLogger(__name__)
    logger.info('Opening csv file: '.format(file_name))
    try:
        file = open(file_name, 'a', newline='')
    except Exception as e:
        logging.exception('Something went wrong opening the csv file.')

    logger.info('Successfully opened csv file.')
    writer = csv.writer(file)

    #  Write information to csv file.
    time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    for column in data_list:
        logger.debug('Writing the following list to csv file: \n {}'
                     .format([time_string] + column))
        writer.writerow([time_string] + column)
        logger.debug('Wrote list.')

    #  Close File
    file.close()
    logger.info('Closed File.')


def ResponseChecker(response: requests.models.Response):
    '''Checks and logs the request response status code of a website.

    Args:
        response (requests.models.Response): A requests response object
        from a requests.get() call to a website.

    Returns:
        None

    Raises:
        None
    '''

    logger = logging.getLogger(__name__)

    if response.status_code != 200:
        logger.error('Failed to connect to: \n {}'
                     .format(response.url))

        logger.debug('Connection Code: {}'.format(response.status_code))
    else:
        logger.info('Successfully connected to : \n {}'
                    .format(response.url))


if __name__ == '__main__':
    data = CollectData()
    WriteData(data)
