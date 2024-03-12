import brotli
import json
from seleniumwire import webdriver
import selenium
import csv
import time

driver = webdriver.Chrome()

# driver.get("https://jp.mercari.com/")
driver.get("https://jp.mercari.com/en/search?keyword=macbook&category_id=7&lang=en&price_min=20000&price_max=45000&status=sold_out%7Ctrading") # custom filter

input('Goto desired page and press "ENTER" once products are visible on the page')
request = driver.wait_for_request('https://api.mercari.jp/v2/entities:search')
response = brotli.decompress(request.response.body).decode('utf-8')
items = json.loads(response)["items"]
new_items = []
def get_item_details():
    for item in items:
        item['productLink'] = f"https://jp.mercari.com/item/{item['id']}"
        driver.get(item['productLink'])
        try:
            request = driver.wait_for_request('https://api.mercari.jp/items/get')
            response = brotli.decompress(request.response.body).decode('utf-8')
            data = json.loads(response)["data"]
            item["description"] = data.get("description", "Not Available")
            print(item["name"])
        except Exception as e:
            print(e)
            print("description not found")
            item["description"] = "Not Available"
            time.sleep(1)
        del driver.requests

def write_to_csv(file_name, rows):
    with open(file_name, 'w', newline='') as file:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

get_item_details()            
write_to_csv("items.csv", items)
print("created \"items.csv\" successfully!")