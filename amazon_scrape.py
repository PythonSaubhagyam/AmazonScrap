from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
DRIVER_PATH = str(Path('chromedriver').resolve())

name_list = []
brand_name_list = []

def get_html(url):
    browser = webdriver.Chrome(executable_path=DRIVER_PATH)
    browser.get(url)
    return browser.page_source

def get_product_name(link):
    url = link
    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')

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


def get_product_brand(link):  # Change class for brand name
    url = link
    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')
    if soup.find_all('span', {'class': 'a-column a-span6'}):
        brand_name1 = soup.find_all('span', {'class': 'a-column a-span6'})
        brand_name = brand_name1[0].text
        brand_name_list.append(brand_name)

    elif soup.find_all('div', {'class': 'a-column a-span6'}):
        brand_name2 = soup.find_all('div', {'class': 'a-column a-span6'})
        brand_name = brand_name2[0].text
        brand_name_list.append(brand_name)

    else:
        brand_name_list.append('Brand Not Found')

    return brand_name_list


if __name__ == '__main__':
    df = pd.read_excel('book2.xls', index_col=0)
    df.drop([ 'INDIVIDUELL2', 'INDIVIDUELL3', 'INDIVIDUELL4', 'INDIVIDUELL5', 'INDIVIDUELL6', 'INDIVIDUELL7', 'INDIVIDUELL8', 'INDIVIDUELL9', 'INDIVIDUELL10', 'INDIVIDUELL11', 'INDIVIDUELL12', 'INDIVIDUELL13', 'INDIVIDUELL14', 'INDIVIDUELL15', 'INDIVIDUELL16', 'INDIVIDUELL17', 'INDIVIDUELL18', 'INDIVIDUELL19', 'INDIVIDUELL20'], axis=1, inplace=True)
    ean_float_list = df['EAN'].tolist()
    ean_list = []
    for ean in ean_float_list:
        ean_split = str(ean).split(".")
        ean_number = ean_split[0]
        ean_list.append(ean_number)
        # print(ean_number)
    count = 0
    for ean_number in ean_list:
        product_names = get_product_name("https://www.amazon.de/s?k=" + ean_number)
        print(product_names)
        if product_names[count] != 'Product Not Found':
            product_brand_name = ((product_names[count]).split())[0]
            brand_name_list.append(str(product_brand_name))
            count+=1
        else:
            brand_name_list.append('Brand Not Found')
            count+=1
        print(brand_name_list)

        # product_brands = get_product_brand("https://www.amazon.de/s?k=" + ean_number)
        # print(product_brands)
    df.drop(['EAN'], axis=1, inplace=True)
    df['ARTIKELNR'] = product_names
    df['BRAND'] = brand_name_list
    df['EAN']= ean_list
    df1=df.reindex(columns=['DBINDEX', 'ARTIKELNR','MWSTART','INDIVIDUELL1','BRAND', 'EAN', 'VK PREIS', 'EK PREIS'])
    df1.to_csv('Exports.csv', float_format='{:f}'.format, encoding='utf-8')


