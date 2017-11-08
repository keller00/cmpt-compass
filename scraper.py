import pprint
import requests
from lxml import html
from json import dumps

url = "http://www.mto.gov.on.ca/english/traveller/trip/traffic_cameras_list.shtml"


def scrape():
    scraped_data = {}
    # Get data
    tree = html.fromstring(requests.get(url).content)
    links = tree.xpath('//div[@class="middleBoxContent"]//a')
    # Extract data
    current = None
    for link in links:
        if 'name' in link.attrib:
            current = link.attrib['name']
            scraped_data[current] = []
        elif 'href' in link.attrib:
            picture_url = link.attrib['href']
            if not picture_url.startswith("#"):
                scraped_data[current].append(picture_url.split('?')[0])

    pprint.PrettyPrinter(depth=2).pprint(scraped_data)
    if input("Does this look correct?(y/n): ").lower() == 'y':
        # Write to file
        with open('links.json', 'w') as output:
            output.write(dumps(scraped_data))

if __name__ == '__main__':
    scrape()
