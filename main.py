from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import csv
DRIVER_PATH = str(Path('chromedriver').resolve())

df = pd.read_excel('Export.xls', index_col=0)
ean_float_list = df['EAN'].tolist()
ean_list = []
for ean in ean_float_list:
    ean_split = str(ean).split(".")
    ean_number = ean_split[0]
    ean_list.append(ean_number)

# Uncomment this to print the list of EAN numbers in the excel file
# print(ean_list)

name_list = []

def get_html(url):
    browser = webdriver.Chrome(executable_path=DRIVER_PATH)
    browser.get(url)
    return browser.page_source

def main(link):
    url = link
    html = get_html(url)

    soup = BeautifulSoup(html,'lxml')
    if soup.find_all('span', {'class': 'a-size-base-plus a-color-base a-text-normal'}):
        name1 = soup.find_all('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
        name = name1[0].text
        name_list.append(name)

    elif soup.find_all('div', {'class': 'a-size-base-plus a-color-base a-text-normal'}):
        name2 = soup.find_all('div', {'class': 'a-size-base-plus a-color-base a-text-normal'})
        name = name2[0].text
        name_list.append(name)

    else:
        name_list.append('Product Not Found')

    return name_list

if __name__== '__main__':
    for ean_number in ean_list:
        product_details = main("https://www.amazon.de/s?k="+ean_number)
        print(product_details)
    write_df = pd.DataFrame(product_details, columns=['Product Name'])
    write_df.to_csv('Product Details.csv')
