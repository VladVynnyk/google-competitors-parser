import ast
import requests
from openai import OpenAI
from bs4 import BeautifulSoup

from utils import get_random_user_agent, format_price, create_messages_for_ai, create_message_for_getting_one_product_from_ai, is_similar, extract_product_link


class Parser:
    def __init__(self):
        pass

    # it's old selectors
    # ads_pannel = soup.find_all("div", id="bGmlqc")
    # ads_name_headers = soup.html.find_all('h4', class_='fol5Z')
    # ads_prices = soup.find_all('div', class_='pSNTSe')
    # ads_items = soup.find_all("div", class_='pla-unit-container')
    # ads_links = soup.find_all("a", class_="vGg33Ymfm0s__pla-unit-link")
    # ads_images = soup.find_all("div", class_="Gor6zc")
    # ads_sites = soup.find_all("div", class_="BZuDuc")

    def parse_google_ads(self, url: str, name_of_product: str, client_of_ai, isIherb: bool):
        user_agent = get_random_user_agent()
        print("user-agent: ", user_agent)

        headers = {'User-agent': user_agent}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            html_content = response.text

            ads_name_headers, ads_prices, ads_links, ads_sites = self.get_info_from_html(html_content)

            product_names = self.create_list_of_product_names(ads_name_headers)
            product_prices = self.create_list_of_product_prices(ads_prices)
            product_sites = self.create_list_of_product_sites(ads_sites)
            product_links = self.create_list_of_product_links(ads_links)

            info_about_all_products_in_ads = self.structure_all_data_to_dict(product_names, product_prices, product_sites, product_links)
            print("INFORMATION: ", info_about_all_products_in_ads)
            print("Len: ", len(info_about_all_products_in_ads))

            # Here we should understand, which products are relevant
            if isIherb == True:
                messages = create_message_for_getting_one_product_from_ai(name_of_product, product_names)
            else:
                messages = create_messages_for_ai(name_of_product, product_names)
            print("MESSAGES: ", messages)
            
            relevant_products_from_ai = self.send_message_to_ai(messages, client_of_ai)

            try:
                relevant_products_in_list = ast.literal_eval(relevant_products_from_ai)
            except:
                return None
            print("Relevant products: ", relevant_products_in_list)

            result = self.select_relevant_products_from_ads(relevant_products_in_list, info_about_all_products_in_ads)

            print("Len: ", len(result))
            
            sorted_data = dict(sorted(result.items(), key=lambda x: x[1]['price']))
            # {product1: {source: Bigl.ua, price:1000, link:https://}, product2: {source: Bigl.ua, price:1000, link:https://}}
            
            return sorted_data


    def get_info_from_html(self, html_content: str):
        soup = BeautifulSoup(html_content, 'html.parser')

        ads_pannel = soup.find_all("div", id="top-pla-group-inner")
        ads_name_headers = soup.html.find_all('a', class_='pla-unit-title-link')
        ads_prices = soup.find_all('div', class_='T4OwTb')
        ads_items = soup.find_all("div", class_='pla-unit-container')
        ads_links = soup.find_all("a", class_="pla-unit-img-container-link")
        ads_images = soup.find_all("div", class_="Gor6zc")
        ads_sites = soup.find_all("div", class_="LbUacb")
        return ads_name_headers, ads_prices, ads_links, ads_sites

    def create_list_of_product_names(self, headlines_of_ads: list):
        product_names = []
        for a_tag in headlines_of_ads:
            current_name = a_tag.find("span").text
            print("CURRENT NAME: ", current_name)
            product_names.append(current_name)
        return product_names
    
    def create_list_of_product_prices(self, prices_from_ads: list):
        product_prices = []
        for item in prices_from_ads:
            current_price = item.find('span').text
            formatted_price = format_price(current_price)
            print("Current price: ", formatted_price)
            [new_price, another_value] = current_price.split(",")
            numeric_part = ''.join(char for char in new_price if char.isdigit() or char == '.') 
            product_prices.append(float(numeric_part))
        return product_prices
    
    def create_list_of_product_links(self, links_from_ads: list):
        product_links = []
        for link in links_from_ads:
            print("EXTRACTED PRODUCT LINK: ", extract_product_link(link['href']))
            print("SINGLE LINK: ", link['href'])
            current_link = link['href']
            product_links.append(current_link)
        return product_links
    
    def create_list_of_product_sites(self, sites_from_ads: list):
        product_sites = []
        for item in sites_from_ads:
            product_sites.append(item.string)
        return product_sites
    
    def structure_all_data_to_dict(self, product_names, product_prices, product_sites, product_links):
        product_info = {}    
                
        for name, price, site, link in zip(product_names, product_prices, product_sites, product_links):
            if name not in product_info:
                product_info[name] = {}
            product_info[name] = {"site": site, "price": price, "link": link}
        return product_info
    
    def send_message_to_ai(self, messages: list, client_of_ai):
        if len(messages) >= 0: 
            completion = client_of_ai.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages
            )            
            relevant_products = completion.choices[0].message.content
            return relevant_products
        else:
            return []
    
    def select_relevant_products_from_ads(self, relevant_products: list, all_products: list):
        result = {}

        for product in relevant_products:
            if all_products.get(product) is not None:
                print("Key existing: ", product)
                result[product] = all_products.get(product)
            else:
                print("Key is not existing: ", product)
                continue
        return result