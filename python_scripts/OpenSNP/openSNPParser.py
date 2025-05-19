from typing import Dict

from attr import attributes
from selenium import webdriver
from selenium.webdriver.common.by import By

import re
import pandas as pd
import os

from traitlets import Integer


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
            match = re.match(r"user(\d+)_", filename)
            if match is not None:
                user_id = match.group(1)
                users[user_id] = User(user_id)

        return users
    except Exception as e:
        print(f"Error reading directory: {e}")
        return {}


basic_link = "https://web.archive.org/web/20250404012926/https://opensnp.org/users/"

driver = None

if driver is None:
    driver = webdriver.Chrome()  # "./chromedriver.exe")

i = 0

for user in get_users(".").values():
    id = user.id
    driver.get(basic_link + str(id) + "#variations")

    driver.implicitly_wait(10)

    # t = driver.find_element(By.XPATH, '//*[@id="variations"]/div')
    t = driver.find_elements(By.XPATH, '//*[@id="variations"]/div/table/tbody')

    if len(t) > 0:

        for j in range(1, len(t[0].text.split("\n")) + 1):
            u = driver.find_element(By.XPATH, '//*[@id="variations"]/div/table/tbody/tr[' + str(j) + ']/td[1]').text
            v = driver.find_element(By.XPATH, '//*[@id="variations"]/div/table/tbody/tr[' + str(j) + ']/td[2]').text

            user.phenotypes[u] = v

        print (user.id + ": " + user.phenotypes)

    i += 1
    if (i >= 10):
        exit(1)