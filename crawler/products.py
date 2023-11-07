import pandas as pd
import requests
import time
import random
import concurrent.futures
import os
import csv
import json

tmp = []
def export_to_csv(data):
    if(not data):
        print('No data to export')
        return

    header = list(data[0].keys());      
    try:
        with open('./products/10k_3.json', 'w', newline='') as usersFile:
            json.dump(data,usersFile)
        print("Error exporting data to users")
    except Exception as e:
        print(f"Error exporting data to users: {e}")

def process_product_by_link(info: dict):
    # print("call")
    sleep_duration = random.uniform(1, 3)  # Random sleep duration between 1 and 5 seconds
    time.sleep(sleep_duration)
    print('Crawling: ...',info['stt'])
    print(f'https://tiki.vn/api/v2/products/{info["id"]}')
    response = requests.get(f'https://tiki.vn/api/v2/products/{info["id"]}', headers ={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'x-guest-token': '81n0c5t7OCxfZSRNe69uDWGpE3MJrVPd',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
    })


    fields_to_exclude = ["master_id", "url_path", "short_url","type","book_cover","short_description","badges","review_count","badges_new","rating_average","review_text","has_ebook","inventory_type","productset_group_name","is_fresh","is_flower","has_buynow","is_gift_card","salable_type","data_version","day_ago_created","meta_title","meta_description","meta_keywords","is_baby_milk","is_acoholic_drink","warranty_policy","current_seller","other_sellers","specifications","product_links","gift_item_title","services_and_promotions","installment_info_v2","is_seller_in_chat_whitelist","warranty_info","inventory","return_and_exchange_policy","is_tier_pricing_available","is_tier_pricing_eligible","benefits","asa_cashback_widget","sku","promotions"]

    if(response.status_code==200):
        filtered_data = {key: value for key, value in response.json().items() if key not in fields_to_exclude}
        tmp.append(filtered_data)


    print(f'Save file successfully')

def parallel_get_categories(df_link):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_product_by_link, df_link.to_dict('records'))
    export_to_csv(tmp)

if __name__ == "__main__":
    df_link = pd.read_csv(
        os.path.join(os.getcwd(), "./dataRaw/test.csv"), delimiter=','
       )

    parallel_get_categories(df_link)
