from typing import Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException
import re
import os
import tempfile
from selenium.webdriver.chrome.options import Options

class User:
    def __init__(self, user_id: str):
        self._id: str = user_id
        self._phenotypes: Dict[str, str] = {}

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def phenotypes(self):
        return self._phenotypes

    @phenotypes.setter
    def phenotypes(self, value):
        self._phenotypes = value

def get_users(directory_path):
    try:
        files = os.listdir(directory_path)
        users = {}
        for filename in files:
            try:
                match = re.match(r"user(\d+)_", filename)
                if match is not None:
                    user_id = match.group(1)
                    users[user_id] = User(user_id)
            except Exception as e:
                print(f"Error processing filename {filename}: {e}")
                continue
        return users
    except Exception as e:
        print(f"Error reading directory: {e}")
        return {}

def main():
    basic_link = "https://web.archive.org/web/20250404012926/https://opensnp.org/users/"
    driver = None
    users = {}
    
    try:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

        driver = webdriver.Chrome(options=options)
        users = get_users(".")

        for user in users.values():
            try:
                id = user.id
                print(f"Parsing user {id}...")
                driver.get(basic_link + str(id) + "#variations")
                driver.implicitly_wait(10)

                t = driver.find_elements(By.XPATH, '//*[@id="variations"]/div/table/tbody')

                if len(t) > 0:
                    print(f"Found {len(t[0].text.split('\n')) - 1} phenotypes for user {id}")
                    for j in range(1, len(t[0].text.split("\n")) + 1):
                        u = driver.find_element(By.XPATH, '//*[@id="variations"]/div/table/tbody/tr[' + str(j) + ']/td[1]').text
                        v = driver.find_element(By.XPATH, '//*[@id="variations"]/div/table/tbody/tr[' + str(j) + ']/td[2]').text

                        user.phenotypes[u] = v
                else:
                    print(f"No phenotypes found for user {id}")

            except (WebDriverException, TimeoutException) as e:
                print(f"Network error or timeout parsing user {id}: {e}")
            except Exception as e:
                print(f"Error parsing user {id}: {e}")

        user_phenotypes = [user.phenotypes for user in users.values()]

        data = dict()

        for user_phenotype in user_phenotypes:
            for phenotype in user_phenotype.keys():
                if phenotype not in data.keys():
                    data[phenotype] = set()
                data[phenotype].add(user_phenotype[phenotype])

        with open("data.csv", "w") as file:
            file.write("User IDs;")
            for phenotype in data.keys():
                file.write(phenotype.strip() + ";")
            file.write("\n")
            file.write("available expressions:;")

            for phenotype in data.keys():
                for expression in data[phenotype]:
                    file.write(expression + ", ")
                file.write(";")
            file.write("\n")

            for user in users.values():
                if len(user.phenotypes) != 0:
                    file.write(user.id + ";")
                    for phenotype in data.keys():
                        if phenotype in user.phenotypes.keys():
                            file.write(user.phenotypes[phenotype])
                        else:
                            file.write("")
                        file.write(";")
                    file.write("\n")

    finally:
        if driver is not None:
            driver.quit()

if __name__ == "__main__":
    main()