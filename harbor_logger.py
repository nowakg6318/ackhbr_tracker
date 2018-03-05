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
    harbor_page = requests.get('') # noqa
    if harbor_page.status_code != 200:
        logger.error('Harbor Page: {}'.format(harbor_page))
    else:
        logger.debug('Harbor Page: {}'.format(harbor_page))
        logger.info('Connected to Harbor Page.')

    soup1 = bs4(harbor_page.content, 'html.parser')
    headers = {'User-Agent': ''} # noqa

    csv_list = []

    #  Grab html from each ship page.
    for ship_tag in soup1.find_all('td', 'name'):
        logger.debug('Finding Ship Name')
        name = ship_tag.text.strip()
        logger.debug('Ship name: {}'.format(name))

        logger.debug('Finding Ship imo')
        imo = ship_tag.find_next_sibling(attrs='lloydsNum').text.strip()
        logger.debug('Ship imo: {}'.format(imo))

        logger.debug('Finding last port of ship.')
        previous_port = (ship_tag.find_next_siblings(attrs='port')[0]
                         .text.strip())
        logger.debug('Previous port of ship: {}'.format(previous_port))

        logger.debug('Finding next port of ship.')
        next_port = ship_tag.find_next_siblings(attrs='port')[1].text.strip()
        logger.debug('Next port of ship: {}'.format(next_port))

        logger.debug('Finding where the ship is docked.')
        dock = (ship_tag.find_next_sibling(attrs='refs').text.strip()
                .split()[0])
        logger.debug('Ship dock: {}'.format(dock))

        if not int(imo):
            continue

        logger.info('Connecting to Ship Page: {}'.format(name))
        ship_page = requests.get('' # noqa
                                 + str(imo), headers=headers)

        if harbor_page.status_code != 200:
            logger.error('Harbor Page: {}'.format(harbor_page))
        else:
            logger.debug('Harbor Page: {}'.format(harbor_page))
            logger.info('Connected to Ship Page: {}'.format(name))

        soup2 = bs4(ship_page.content, 'html.parser')
        logger.info('Grabbing data for {}, imo: {}'.format(name, imo))

        logger.debug('Finding Ship Type')
        ship_type = (soup2.find('a', 'font-120').text.strip())
        logger.debug('Ship Type: {}'.format(ship_type))

        logger.debug('Finding Ship Flag')
        flag = (soup2.find('span', string='Flag: ')
                .find_next_sibling('b').text.strip()[:-5])
        logger.debug('Flag: {}'.format(flag))

        logger.debug('Finding Ship Gross Tonnage')
        gross_tonnage = (soup2.find('span', string='Gross Tonnage: ')
                         .find_next_sibling('b').text.strip())
        logger.debug('Gross Tonnage: {}'.format(ship_type))

        logger.debug('Finding Ship Deadweight Tonnage')
        deadweight_tonnage = (soup2.find('span', string='Deadweight: ')
                              .find_next_sibling('b').text.strip()[:-2])
        logger.debug('Deadweight Tonnage: {}'.format(deadweight_tonnage))
        logger.info('Successfully grabbed information for {}, imo: {}'
                    .format(name, imo))

        ship_list = [name, imo, ship_type, flag, gross_tonnage,
                     deadweight_tonnage, dock, previous_port, next_port]
        logger.debug('List to be appended to csv file: \n {}'
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


if __name__ == '__main__':
    data = CollectData()
    WriteData(data)
