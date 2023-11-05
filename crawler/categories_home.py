import pandas as pd
import requests
import time
import random
import concurrent.futures
import os
import csv
tmp = []
def export_to_csv(data):
    if(not data):
        print('No data to export')
        return

    header = list(data[0].keys());      
    try:
        with open('test.csv', 'w', newline='') as usersFile:
            fileWriter = csv.writer(usersFile, delimiter=',')
            reader = csv.reader('test.csv')
            if(reader.line_num == 0):
                fileWriter.writerow(header)
            for row in data:
                fileWriter.writerow(list(row.values())) 
        print("Error exporting data to users")
    except Exception as e:
        print(f"Error exporting data to users: {e}")

def process_product_by_link(info: dict):
    sleep_duration = random.uniform(1, 2)  # Random sleep duration between 1 and 5 seconds
    time.sleep(sleep_duration)
    print('Crawling: ...',info['categoryId'])
    print(f'https://tiki.vn/api/v2/categories/{info["categoryId"]}')
    response = requests.get(f'https://tiki.vn/api/v2/categories/{info["categoryId"]}?include=ancestors', headers ={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',

    'x-guest-token': '81n0c5t7OCxfZSRNe69uDWGpE3MJrVPd',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
    })

    if(response.status_code==200):
        tmp.append(response.json())


    print(f'Save file successfully')

def parallel_get_categories(df_link):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(process_product_by_link, df_link.to_dict('records'))
    export_to_csv(tmp)

if __name__ == "__main__":
    df_link = pd.read_csv(
        os.path.join(os.getcwd(), "category_home.csv"), delimiter=','
       )
    parallel_get_categories(df_link)
