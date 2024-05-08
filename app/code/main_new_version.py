import time

from difflib import SequenceMatcher
import requests
import heapq
from bs4 import BeautifulSoup
from dotenv import dotenv_values
from openpyxl import load_workbook
from openpyxl import Workbook

from openai import OpenAI

from urllib.parse import urlparse, parse_qs

from Parser import Parser
from utils import get_random_user_agent, format_price, create_messages_for_ai, is_similar, extract_product_link


config = dotenv_values(".env")
CHATGPT_KEY = config["CHATGPT_KEY"]
 
def main():
    parser = Parser()
    client = OpenAI(api_key=CHATGPT_KEY)

    workbook = load_workbook('app/data/Testfile.xlsx')
    source_sheet = workbook.active

    max_row = source_sheet.max_row

    products = []

    
    row_index = 2 
    for col in source_sheet.iter_cols(min_row=2, max_row=max_row, min_col=5, max_col=5):
        for cell in col:
            current_product_name = cell.value
            edited_product_name = current_product_name.replace(" ", "+")
            url = "https://www.google.com/search?q="+edited_product_name
            print(edited_product_name)
            print(url)
            info = parser.parse_google_ads(url, cell.value, client_of_ai=client)
            # {product1: [source, price, link], product2: [source, price, link]}

            print("info:", info)
            time.sleep(10)

            # Вставка значень info в клітинки J, K, L
            if info != None and len(info)>=1:
                source_sheet.cell(row=row_index, column=10).value = info[0][2]  # Значення info[0] у стовпець J
                source_sheet.cell(row=row_index, column=9).value = info[0][1]  # Значення info[0] у стовпець J
                print("SOURCE: ", info[0][0])
                print("PRICE: ", info[0][1])
                print("LINK: ", info[0][2])
                if len(info) == 2 or len(info) >= 2:
                    source_sheet.cell(row=row_index, column=13).value = info[1][2]  # Значення info[1] у стовпець K
                    source_sheet.cell(row=row_index, column=12).value = info[1][1]  # Значення info[1] у стовпець K
                    print("SOURCE: ", info[1][0])
                    print("PRICE: ", info[1][1])
                    print("LINK: ", info[1][2])
                if len(info) == 3:
                    source_sheet.cell(row=row_index, column=16).value = info[2][2]  # Значення info[2] у стовпець L
                    source_sheet.cell(row=row_index, column=15).value = info[2][1]  # Значення info[2] у стовпець L
                    print("SOURCE: ", info[2][0])
                    print("PRICE: ", info[2][1])
                    print("LINK: ", info[2][2])
                if len(info) == 4:
                    source_sheet.cell(row=row_index, column=19).value = info[3][2]  # Значення info[2] у стовпець L
                    source_sheet.cell(row=row_index, column=18).value = info[3][1]  # Значення info[2] у стовпець L
                    print("SOURCE: ", info[2][0])
                    print("PRICE: ", info[2][1])
                    print("LINK: ", info[2][2])
                if len(info) == 5:
                    source_sheet.cell(row=row_index, column=22).value = info[4][2]  # Значення info[2] у стовпець L
                    source_sheet.cell(row=row_index, column=21).value = info[4][1]  # Значення info[2] у стовпець L
                    print("SOURCE: ", info[2][0])
                    print("PRICE: ", info[2][1])
                    print("LINK: ", info[2][2])
                row_index += 1
            else:
                row_index += 1
                continue


    # workbook.save('./Testfile.xlsx')
    workbook.save('./Оборотні_профільних_ціни_конкурентів_для_HF.xlsx')


main()