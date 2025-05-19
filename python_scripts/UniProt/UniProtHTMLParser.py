from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import sqlite3
from urllib.request import urlopen
import json
import time

class UniProtHTMLParser:
    def __init__(self, file):
        self.db = sqlite3.connect(file)
        self.cursor = self.db.cursor()

        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        # Initialize the driver
        self.driver = webdriver.Chrome(options=chrome_options)

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

    def wait_for_content(self):
        wait = WebDriverWait(self.driver, 10)
        try:
            # Wait for tables
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'WjGBm')))
            # Wait for headers
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h4')))
            return True
        except Exception as e:
            print(f"Timeout waiting for content: {e}")
            return False

    def load_html(self, url):
        try:
            print(f"Loading URL: {url}")
            self.driver.get(url)

            if not self.wait_for_content():
                return None

            # Scroll to ensure all lazy-loaded content is loaded
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # Additional wait for any lazy-loaded content
            time.sleep(2)

            page_source = self.driver.page_source
            return BeautifulSoup(page_source, 'html.parser')

        except Exception as e:
            print(f"Error fetching URL {url}: {e}")
            return None
        finally:
            self.driver.delete_all_cookies()

    def parse_disease_and_rs(self, soup):
        results = []

        # Find all disease headers
        disease_headers = soup.find_all('h4')

        for i, header in enumerate(disease_headers):
            disease_name = header.a.text.strip() if header.a else None
            if not disease_name:
                continue

            # Get the next header to establish our boundary
            next_header = disease_headers[i + 1] if i + 1 < len(disease_headers) else None

            # Find the next table within bounds
            current = header
            while current:
                current = current.find_next()
                # Stop if we hit the next header or end of document
                if not current or (next_header and current == next_header):
                    break

                if current.name == 'table' and 'WjGBm' in current.get('class', []):
                    # Search for rs ID in the table
                    td_elements = current.find_all('td')
                    for td in td_elements:
                        text = td.text.strip()
                        if 'dbSNP:rs' in text:
                            rs_id = text.split('dbSNP:rs')[1].split()[0].strip()
                            result = {
                                'disease': disease_name,
                                'rs_id': rs_id
                            }
                            if result not in results:  # Avoid duplicates
                                results.append(result)
                    break  # Found our table, no need to continue searching
        return results

    def get_protein_variants(self, protein_id):
        url = f"https://www.uniprot.org/uniprotkb/{protein_id}/entry#disease_variants"
        soup = self.load_html(url)
        if soup:
            return self.parse_disease_and_rs(soup)
        return []

    def get_rsIDs_from_db(self):
        self.cursor.execute("SELECT rs_ID FROM SNP_TABLE")
        return [row[0] for row in self.cursor.fetchall()]

    def get_primaryAccessions_for_rsID(self, rs_ID):
        url = f"https://rest.uniprot.org/uniprotkb/search?query=(xref:dbsnp-rs{rs_ID})"
        request = urlopen(url).read().decode("utf-8")
        data = json.loads(request)
        primary_accessions = list()

        if 'results' in data and data['results']:
            for result in data['results']:
                if 'primaryAccession' in result:
                    primary_accessions.append(result['primaryAccession'])
        return primary_accessions

    def run(self):
        rsIDs = self.get_rsIDs_from_db()
        for rsID in rsIDs:
            primaryAccessions = self.get_primaryAccessions_for_rsID(rsID)

            if primaryAccessions is not None:
                for EntryID in primaryAccessions:
                    data = self.get_protein_variants(EntryID)
                    for result in data:
                        exit
                        disease_present = self.cursor.execute("SELECT * FROM DISEASE_TABLE WHERE Disease = ?",
                                                              (result['disease'],)).fetchone()

                        if disease_present is None:
                            self.cursor.execute("INSERT INTO DISEASE_TABLE (Disease) VALUES (?)", (result['disease'],))
                            self.db.commit()

                        rsID_present = self.cursor.execute("SELECT rs_ID FROM SNP_TABLE WHERE rs_ID = ?",
                                                      (result['rs_id'],)).fetchone()
                        if rsID_present is None:
                            self.cursor.execute("INSERT INTO SNP_TABLE (rs_ID) VALUES (?);", (result['rs_id'],))
                            self.db.commit()
                    print(f"Found {len(data)} disease-variant associations for {EntryID}")


if __name__ == "__main__":
    parser = UniProtHTMLParser("SNP2Pheno.db")
    parser.run()