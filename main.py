from difflib import SequenceMatcher
import requests
import heapq
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from openpyxl import Workbook

def is_similar(a, b):
     return SequenceMatcher(None, a, b).ratio()

def parse_google_ads(url: str, name_of_product: str):
    response = requests.get(url)
    # print(response)
 
    if response.status_code == 200:
            # Отримуємо HTML-вміст сторінки
            html_content = response.text
 
            # Створюємо об'єкт BeautifulSoup для парсингу
            soup = BeautifulSoup(html_content, 'html.parser')
 
            # Знаходимо елементи, які містять рекламу
            # ads = soup.find_all('div', class_='ads')

            ads_pannel = soup.find_all("div", id="bGmlqc")
            # ads_name_headers = soup.html.find_all('span', class_='pymv4e', recursive=False)
            ads_name_headers = soup.html.find_all('h4', class_='fol5Z')
            # ads_prices = soup.find_all('div', class_='qptdjc')
            ads_prices = soup.find_all('div', class_='pSNTSe')
            ads_items = soup.find_all("div", class_='pla-unit-container')
            ads_links = soup.html.find_all("a", class_="pla-unit-link")
            ads_images = soup.find_all("div", class_="Gor6zc")
            ads_sites = soup.find_all("div", class_="BZuDuc")

            # print("Ads pannel: ", ads_pannel)
            # print("Names: ", ads_name_headers)            
            # print("Prices: ", ads_prices)      
            # print("Items: ", ads_items)      
            # print("Links: ", ads_links)
            # print("Images", ads_images)
            # print("Site: ", ads_sites)

            product_names = []
            product_prices = []
            product_sites = []

            for item in ads_images:
                print("IMAGES: -------------------------")
                current_name = item.img['alt']
                current_name[20:]
                print(current_name[18:])
                product_names.append(current_name[18:])


            for item in ads_prices:
                current_price = item.string
                [new_price, another_value] = current_price.split(",")
                numeric_part = ''.join(char for char in new_price if char.isdigit() or char == '.') 
                # print(float(numeric_part))
                # print(new_price)
                # print("---------------------------------------")
                product_prices.append(float(numeric_part))

            for item in ads_sites:
                # print("ITEM: ", item.string)
                product_sites.append(item.string)
            

            # dict_of_items = dict(zip(product_names, product_prices))
            # for product, price in dict_of_items.items():
            #     print(f'{product}: {price}')
                
            product_info = {}    
                
            for name, price, site in zip(product_names, product_prices, product_sites):
                if name not in product_info:
                    product_info[name] = []
                product_info[name].append([site, price])

            # print(product_info)

            # STEPS: 
            # 1.Search for the cheapest products on the ads
            # 2.Write them to excel
            # 3.Search for the products on the iherb
            
            # 1.
            workbook = load_workbook('D:\TEST OF MY JOB\EXCEL\Competitors parser\Каста ціни – копія.xlsx')
            source_sheet = workbook.active



            smallest_values = heapq.nsmallest(2, product_prices)
            print("Smallest values: ", smallest_values)

            smallest_products = []
            for item in product_info:
                for y in smallest_values:
                    print(item, product_info[item])
                    print("Y:", y)
                    if y == product_info[item][0][1]:
                        print("How similar: ", is_similar(name_of_product, item))
                        if is_similar(name_of_product, item) >= 0.3:
                            smallest_products.append(item)
            
            result = []
            for product in smallest_products:
                print("One of the cheapest products: ", product, product_info[product])
                result.append(product_info[product])
                # return product_info[product]
            return result

 
# parse_google_ads("https://www.google.com/search?q=protein+whey")
# parse_google_ads("https://www.google.com/search?client=opera&q=protein+whey&sourceid=opera&ie=UTF-8&oe=UTF-8")


def main():
    workbook = load_workbook('D:\TEST OF MY JOB\EXCEL\Competitors parser\Каста ціни – копія.xlsx')
    source_sheet = workbook.active

    products = []

    # for col in source_sheet.iter_cols(min_row=2, max_row=58, min_col=5, max_col=5):
    #     for cell in col:
    #         current_product_name = cell.value
    #         edited_product_name = cell.value.replace(" ", "+")
    #         url = "https://www.google.com/search?client=opera&q="+edited_product_name+"&sourceid=opera&ie=UTF-8&oe=UTF-8"
    #         print(edited_product_name)
    #         print(url)
    #         info = parse_google_ads(url)
    #         products.append(info)
    
    row_index = 2 
    for col in source_sheet.iter_cols(min_row=2, max_row=58, min_col=5, max_col=5):
        for cell in col:
            current_product_name = cell.value
            edited_product_name = current_product_name.replace(" ", "+")
            url = "https://www.google.com/search?client=opera&q="+edited_product_name+"&sourceid=opera&ie=UTF-8&oe=UTF-8"
            print(edited_product_name)
            print(url)
            info = parse_google_ads(url, cell.value)

            # Вставка значень info в клітинки J, K, L
            print("info:", info)
            if info != None and len(info)>1:
                source_sheet.cell(row=row_index, column=10).value = info[0][0][0]  # Значення info[0] у стовпець J
                source_sheet.cell(row=row_index, column=11).value = info[0][0][1]  # Значення info[0] у стовпець J
                if len(info[0]) == 3:
                    source_sheet.cell(row=row_index, column=12).value = info[0][1][1]  # Значення info[1] у стовпець K
                if len(info[0]) == 4:
                    source_sheet.cell(row=row_index, column=13).value = info[0][2][1]  # Значення info[2] у стовпець L
                row_index += 1
            else:
                row_index += 1
                continue

            # row_index += 1  # Збільшення індексу рядка для наступної вставки

    workbook.save('D:\TEST OF MY JOB\EXCEL\Competitors parser\Каста ціни – копія.xlsx')


main()