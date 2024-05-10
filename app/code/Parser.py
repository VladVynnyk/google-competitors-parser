import ast
import requests
from openai import OpenAI
from bs4 import BeautifulSoup

from utils import get_random_user_agent, format_price, create_messages_for_ai, is_similar, extract_product_link


class Parser:
    def __init__(self):
        pass

    # This method returns ads with lowest price
    def parse_google_ads(self, url: str, name_of_product: str, client_of_ai):
        # {product1: {source: Bigl.ua, price:1000, link:https://}, product2: {source: Bigl.ua, price:1000, link:https://}}
        user_agent = get_random_user_agent()

        print("user-agent: ", user_agent)

        headers = {'User-agent': user_agent}


        response = requests.get(url, headers=headers)

        # with open("demofile2.txt", "w", encoding="utf-8") as f:
        #     f.write(response.text)
    
        if response.status_code == 200:
                html_content = response.text
    
                soup = BeautifulSoup(html_content, 'html.parser')

                # it's old selectors
                # ads_pannel = soup.find_all("div", id="bGmlqc")
                # ads_name_headers = soup.html.find_all('h4', class_='fol5Z')
                # ads_prices = soup.find_all('div', class_='pSNTSe')
                # ads_items = soup.find_all("div", class_='pla-unit-container')
                # ads_links = soup.find_all("a", class_="vGg33Ymfm0s__pla-unit-link")
                # ads_images = soup.find_all("div", class_="Gor6zc")
                # ads_sites = soup.find_all("div", class_="BZuDuc")


                ads_pannel = soup.find_all("div", id="top-pla-group-inner")
                ads_name_headers = soup.html.find_all('a', class_='pla-unit-title-link')
                ads_prices = soup.find_all('div', class_='T4OwTb')
                ads_items = soup.find_all("div", class_='pla-unit-container')
                ads_links = soup.find_all("a", class_="pla-unit-img-container-link")
                ads_images = soup.find_all("div", class_="Gor6zc")
                ads_sites = soup.find_all("div", class_="LbUacb")

                

                product_names = []
                product_prices = []
                product_sites = []
                product_links = []

                for a_tag in ads_name_headers:
                    current_name = a_tag.find("span").text
                    print("CURRENT NAME: ", current_name)
                    product_names.append(current_name)


                for link in ads_links:
                    print("EXTRACTED PRODUCT LINK: ", extract_product_link(link['href']))
                    print("SINGLE LINK: ", link['href'])
                    current_link = link['href']
                    product_links.append(current_link)


                for item in ads_prices:
                    current_price = item.find('span').text
                    formatted_price = format_price(current_price)
                    print("Current price: ", formatted_price)
                    [new_price, another_value] = current_price.split(",")
                    numeric_part = ''.join(char for char in new_price if char.isdigit() or char == '.') 
                    product_prices.append(float(numeric_part))

                for item in ads_sites:
                    product_sites.append(item.string)
                    
                product_info = {}    
                    
                for name, price, site, link in zip(product_names, product_prices, product_sites, product_links):
                    if name not in product_info:
                        product_info[name] = []
                    product_info[name].append([site, price, link])

                print("INFORMATION: ", product_info)

                # Here we should understand, which products are relevant
                messages = create_messages_for_ai(name_of_product, product_names)
                print("MESSAGES: ", messages)
                if len(messages) > 0: 
                    completion = client_of_ai.chat.completions.create(
                        model="gpt-3.5-turbo-0125",
                        messages=messages
                    )            
                
                relevant_products = completion.choices[0].message.content
                print("Relevant products: ", relevant_products)
                print("Relevant products: ", type(relevant_products))
                print("Relevant products: ", type(list(relevant_products)))


                smallest_values = sorted(product_prices, reverse=True)

                smallest_products = []
                for item in product_info:
                    for y in smallest_values:
                        if y == product_info[item][0][1]:
                            if item in list(relevant_products):
                                if item not in smallest_products:
                                    smallest_products.append(item)
                                else: continue

                print("--------------------------------")
                print("Cheapest products: ", smallest_products)
                print("Length of cheapest products: ", len(smallest_values))
                result = []

                for product in smallest_products:
                    print("One of the cheapest products: ", product, product_info[product])
                    result.append(product_info[product][0])
                return result
        


    # This method returns ads with lowest price
    def parse_google_ads(self, url: str, name_of_product: str, client_of_ai):
        user_agent = get_random_user_agent()

        print("user-agent: ", user_agent)

        headers = {'User-agent': user_agent}


        response = requests.get(url, headers=headers)

        # with open("demofile2.txt", "w", encoding="utf-8") as f:
        #     f.write(response.text)
    
        if response.status_code == 200:
                html_content = response.text
    
                soup = BeautifulSoup(html_content, 'html.parser')

                ads_pannel = soup.find_all("div", id="top-pla-group-inner")
                ads_name_headers = soup.html.find_all('a', class_='pla-unit-title-link')
                ads_prices = soup.find_all('div', class_='T4OwTb')
                ads_items = soup.find_all("div", class_='pla-unit-container')
                ads_links = soup.find_all("a", class_="pla-unit-img-container-link")
                ads_images = soup.find_all("div", class_="Gor6zc")
                ads_sites = soup.find_all("div", class_="LbUacb")

                product_names = []
                product_prices = []
                product_sites = []
                product_links = []

                for a_tag in ads_name_headers:
                    current_name = a_tag.find("span").text
                    print("CURRENT NAME: ", current_name)
                    product_names.append(current_name)


                for link in ads_links:
                    print("EXTRACTED PRODUCT LINK: ", extract_product_link(link['href']))
                    print("SINGLE LINK: ", link['href'])
                    current_link = link['href']
                    product_links.append(current_link)


                for item in ads_prices:
                    current_price = item.find('span').text
                    formatted_price = format_price(current_price)
                    print("Current price: ", formatted_price)
                    [new_price, another_value] = current_price.split(",")
                    numeric_part = ''.join(char for char in new_price if char.isdigit() or char == '.') 
                    product_prices.append(float(numeric_part))

                for item in ads_sites:
                    product_sites.append(item.string)
                    
                product_info = {}    
                    
                for name, price, site, link in zip(product_names, product_prices, product_sites, product_links):
                    if name not in product_info:
                        product_info[name] = {}
                    product_info[name] = {"site": site, "price": price, "link": link}

                print("INFORMATION: ", product_info)
                print("Len: ", len(product_info))

                # Here we should understand, which products are relevant
                messages = create_messages_for_ai(name_of_product, product_names)
                print("MESSAGES: ", messages)
                if len(messages) >= 0: 
                    completion = client_of_ai.chat.completions.create(
                        model="gpt-3.5-turbo-0125",
                        messages=messages
                    )            
                
                relevant_products = completion.choices[0].message.content
                # relevant_products = list(relevant_products)
                relevant_products = ast.literal_eval(relevant_products)
                print("Relevant products: ", relevant_products)

                result = {}

                for product in relevant_products:
                    if product_info.get(product) is not None:
                        print("Key existing: ", product)
                        result[product] = product_info.get(product)
                    else:
                        print("Key is not existing: ", product)
                        continue

                print("Len: ", len(result))
                
                sorted_data = dict(sorted(result.items(), key=lambda x: x[1]['price']))
                # {product1: {source: Bigl.ua, price:1000, link:https://}, product2: {source: Bigl.ua, price:1000, link:https://}}
                
                return sorted_data