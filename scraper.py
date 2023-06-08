import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib.parse

subjects = [
    "https://gceguide.com/papers/A%20Levels/Accounting%20(9706)/",
    "https://gceguide.com/papers/A%20Levels/Biology%20(9700)/",
    "https://gceguide.com/papers/A%20Levels/Chemistry%20(9701)/",
    "https://gceguide.com/papers/A%20Levels/Computer%20Science%20(for%20final%20examination%20in%202021)%20(9608)/",
    "https://gceguide.com/papers/A%20Levels/Computing%20(9691)/",
    "https://gceguide.com/papers/A%20Levels/Economics%20(9708)/",
    "https://gceguide.com/papers/A%20Levels/English%20-%20Language%20and%20Literature%20(AS%20Level%20only)%20(8695)/",
    "https://gceguide.com/papers/A%20Levels/English%20-%20Literature%20(9695)/",
    "https://gceguide.com/papers/A%20Levels/Information%20Technology%20(9626)/",
    "https://gceguide.com/papers/A%20Levels/Physics%20(9702)/",
    "https://gceguide.com/papers/A%20Levels/Psychology%20(9698)/",
    "https://gceguide.com/papers/A%20Levels/Psychology%20(9990)/",
]


def scrape_years(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Get the HTML content from the response
    html_content = response.content
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, "html.parser")
    try:
        # Find the <ul> element with id="paperslist"
        ul_element = soup.find("ul", {"id": "paperslist"})
        # Find all <a> tags within the <ul> element
        links = ul_element.find_all("a")
        # Extract the href attribute from each <a> tag
        link_urls = [link["href"] for link in links]
        # Remove anything that isn't an year (numbers only)
        link_urls = [link for link in link_urls if link.isdigit()]
        # url + year = full url
        link_urls = [url + year for year in link_urls]
        return link_urls
    except AttributeError:
        print(f"Error: {url} does not exist")
        return []

def scrape_papers(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Get the HTML content from the response
    html_content = response.content
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, "html.parser")
    try:
        # Find the <ul> element with id="paperslist"
        ul_element = soup.find("ul", {"id": "paperslist"})
        # Find all <li> tags within the <ul> element
        li_elements = ul_element.find_all('li')
        # Extract the href attribute from each <a> tag within the <li> elements
        link_urls = []
        for li in li_elements:
            link = li.find('a')
            if link:
                link_urls.append(link['href'])
        # url + pdf name = full url
        link_urls = [url + '/' + link for link in link_urls]
        return link_urls
    except AttributeError:
        print(f"Error: {url} does not exist")
        return []
    
master_pdf_list = []

for subject in tqdm(subjects, desc="Scraping Subjects", unit="subject"):
    years = scrape_years(subject)
    for year in tqdm(years, desc=f"Scraping Papers for {urllib.parse.unquote(subject.split('/')[-2])}", unit="year", leave=False):
        papers = scrape_papers(year)
        for paper in papers:
            master_pdf_list.append(paper)

# Save to file
with open('master_pdf_list.txt', 'w') as f:
    for item in master_pdf_list:
        f.write("%s\n" % item)