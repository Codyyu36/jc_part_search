from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup as soup

app = Flask(__name__)

root_url = "https://octopart.com/search?q="

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
        print(item)
    return info_list, data
        
def scrape_page(part_no):

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(root_url + part_no)

    print(response.status_code)
    # print(response.text)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    # creating a soup object from the returned html page
    sp = soup(response.text, "lxml")
    sp.prettify

    # getting the title/part number info
    # title_div = sp.findAll('div', class_='flex items-end gap-7')  # Adjust the class if necessary
    # getting the prices
    # table = sp.findAll('table', class_='w-full border-collapse text-base')  # Adjust class if necessary
    # check data 
    # if (len(table) != len(title_div)):
    #     print("Data misaligned, infomation could be incorrect, please check it on https://www.octopart.com/ manually.")
    
        # Extract the title information
    title_div = sp.find('div', class_='flex items-end gap-7')
    if title_div:
        mark_text = title_div.find('mark').text.strip() if title_div.find('mark') else ''
        span_text = title_div.find('span', class_='').text.strip() if title_div.find('span', class_='') else ''
        # title = f"{mark_text} {span_text}"
        title = mark_text
    else:
        title = "Title not found"

    # Locate the table
    table = sp.find('table', class_='w-full border-collapse text-base')
    if not table:
        return title, ["Table not found"]

    # Extract data from the table
    data = []
    # Generate column headers
    table_headers = [
        "Distributor", "Part number", "Stock", "MOQ", "Pkg", "Price in", 
        "Price for 1", "Price for 10", "Price for 100", "Price for 1,000", 
        "Price for 10,000", "Last update"
    ]
    data.append(table_headers)

    for row in table.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        if len(cols) >= 14:
            # Extract only the relevant fields based on the specified indices
            row_data = [
                cols[1].text.strip(), cols[3].text.strip(), cols[4].text.strip(), 
                cols[5].text.strip(), cols[6].text.strip(), cols[7].text.strip(), 
                cols[8].text.strip(), cols[9].text.strip(), cols[10].text.strip(), 
                cols[11].text.strip(), cols[12].text.strip(), cols[13].text.strip()
            ]
            data.append(row_data)
    return title, data






@app.route('/new_page', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        title, data = scrape_page(url)
        return render_template('index.html', title=title, data=data)
    return render_template('index.html', title=None, data=None)

@app.route('/', methods=['GET', 'POST'])
def old():
    if request.method == 'POST':
        url = request.form['url']
        title, data = scrape_page(url)
        return render_template('old.html', title=title, data=data)
    return render_template('old.html', title=None, data=None)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
