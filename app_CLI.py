# importing the libraries

import requests
from bs4 import BeautifulSoup as soup
url = "https://octopart.com/search?q="

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.octopart.com/",
}

def print_info(info_list, table, length):
    #for i in range(0, length):

        #for j in range(0, len(info_list)):

    # Step 4: Extract data from the table
    data = []
    for row in table.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols])  # Get rid of empty values

    # Print the extracted data
    for item in data:
        entry = "Distributor: %s\nPart number: %s\nStock: %s\nMOQ: %s\nPkg: %s\nPrice in: %s\nPrice for 1: %s\nPrice for 10: %s\nPrice for 100: %s\nPrice for 1000: %s\nPrice for 10000: %s\nLast update: %s\n" % (item[1], item[3], item[4], item[5], item[6], item[7],item[8],item[9], item[10], item[11],item[12],item[13])
        print(entry)
        # print(item)
        
def scrape_page(part_no):

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url + part_no)

    # print(response.status_code)
    # print(response.text)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    # creating a soup object from the returned html page
    sp = soup(response.text, "lxml")
    sp.prettify

    # getting the title/part number info
    title_div = sp.findAll('div', class_='flex items-end gap-7')  # Adjust the class if necessary
    # getting the prices
    table = sp.findAll('table', class_='w-full border-collapse text-base')  # Adjust class if necessary
    # check data 
    if (len(table) != len(title_div)):
        print("Data misaligned, infomation could be incorrect, please check it on https://www.octopart.com/ manually.")
    
    print_info([], table[0], len(table))




if __name__ == "__main__":
    while True:
        print("Enter the part number: ")
        print("(or enter 'Q' to quit)")
        part_no = input()
        if part_no.strip().upper() == 'Q':
            print("Exiting the scraper. Goodbye!")
            break
        scrape_page(part_no)