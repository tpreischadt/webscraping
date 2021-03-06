from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager

import json

class LinkedinScraper:

    def __init__(self, queries):

        '''
        Parameters
        ------------

        queries: list
            list containing linkedin queries. Ex: Data Scientist São Paulo
        
        '''

        self.setup()
        self.queries = queries

    def setup(self):
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

    def scrape(self):
        for query in self.queries:
            lookup = 'site:linkedin.com/in ' + query.strip()
            users = self.search(lookup, num_pages=5)
        
        return users
    
    def search(self, query, num_pages=5):

        '''
        Get all results from a certain query in the first few pages.

        Parameters
        ------------

        query: str
        
        num_pages: int
            Number of pages to be scraped for each lookup

        Return
        ---------

        user: list
            List containing all user URLs
        '''

        self.driver.get('http://www.google.com')

        search_box = self.driver.find_element_by_name('q')
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)
    
        URLs = set()
        for _ in range(num_pages - 1):
            # wait for results to show up
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'result-stats')))

            results = self.driver.find_elements_by_css_selector('div.g')

            # get href results
            for r in results:
                profile_element = r.find_element_by_css_selector('div.r')
                profile = profile_element.find_element_by_tag_name('a')
                URLs.add(profile.get_attribute('href'))
            
            next_button = self.driver.find_element_by_id('pnnext')
            next_button.click()
        
        return list(URLs)

if __name__ == '__main__':

    # Reading queries file
    try:
        with open('queries.in', 'r') as f:
            queries = f.readlines()
    except FileNotFoundError:
        print(f'File queries.in should contain queries.')
        exit(-1)

    scraper = LinkedinScraper(queries)
    scraped_users = scraper.scrape()

    output = {"profiles": scraped_users}

    with open('users.json', 'w') as f:
        f.write(json.dumps(output))