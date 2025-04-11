from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json


base_url = "https://gantoum.ir/Search/3/%D8%AF%D8%B3%D8%AA%D9%87-%D8%A8%D9%86%D8%AF%DB%8C-%D9%85%D8%AD%D8%B5%D9%88%D9%84%D8%A7%D8%AA?pageId={}&brands=&attributes=&hasSellingStock=false&startPrice=0&endPrice=1350000&sortBy="

def scrape_products(**kwargs):
    def get_product_data_from_page(page_number):
        url = base_url.format(page_number)
        print(f"Scraping page {page_number}: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()  
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page_number}: {e}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find(id="products")

        if not results:
            print(f"No products found on page {page_number}. Stopping.")
            return None

        products_data = []
        non = results.find_all("div", class_="col-product-pg")

        for i in non:
            name = i.find("h3", class_="ti-pr-pg").text.strip()
            price = i.find("span", class_="price-bx").text.strip()
            image_element = i.find("img")
            image_url = image_element['src'] if image_element and 'src' in image_element.attrs else None

            product = {
                "name": name,
                "price": price,
                "image_url": image_url
            }

            products_data.append(product)
            print(price, name, image_url)

        return products_data

    all_products = []
    page_number = 1

    while True:
        print(f"\nProcessing page {page_number}...")
        products = get_product_data_from_page(page_number)

        if not products:
            break

        all_products.extend(products)
        page_number += 1

    print(f"Scraped {len(all_products)} products.")
    return all_products

def save_to_json(ti, **kwargs):
    all_products = ti.xcom_pull(task_ids='scrape_products')

    if not all_products:
        print("No products to save to JSON.")
        return

    output_file = "/opt/airflow/dags/gantum_products1.json"

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_products, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {output_file} with {len(all_products)} products.")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")
        raise

def save_to_database(ti, **kwargs):
    postgres_hook = PostgresHook(postgres_conn_id='gantoum_postgres')

    create_table_query = """
    CREATE TABLE IF NOT EXISTS public.products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price VARCHAR(50) NOT NULL,
        image_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    truncate_table_query = """
    TRUNCATE TABLE public.products RESTART IDENTITY;
    """

    try:
        print("Setting search_path to public...")
        postgres_hook.run("SET search_path TO public;")

        print("Creating table 'products' in public schema if it doesn't exist...")
        postgres_hook.run(create_table_query)

        print("Truncating table 'products' to remove old data...")
        postgres_hook.run(truncate_table_query)

    except Exception as e:
        print(f"Error setting up the table: {e}")
        raise

    all_products = ti.xcom_pull(task_ids='scrape_products')

    if not all_products:
        print("No products to save to database.")
        return

    insert_query = """
        INSERT INTO public.products (name, price, image_url)
        VALUES (%s, %s, %s)
    """

    try:
        for product in all_products:
            if not product["name"] or not product["price"]:
                print(f"Skipping invalid product: {product}")
                continue
            postgres_hook.run(insert_query, parameters=(
                product["name"],
                product["price"],
                product["image_url"]
            ))
        print(f"Successfully inserted {len(all_products)} products into the database.")
    except Exception as e:
        print(f"Error inserting data into database: {e}")
        raise

with DAG(
    dag_id='load_products',
    start_date=datetime(2025, 4, 11),
    schedule_interval='@daily',  
    catchup=False,
) as dag:

    scrape_task = PythonOperator(
        task_id='scrape_products',
        python_callable=scrape_products,
    )

    save_json_task = PythonOperator(
        task_id='save_to_json',
        python_callable=save_to_json,
    )

    save_db_task = PythonOperator(
        task_id='save_to_database',
        python_callable=save_to_database,
    )

    scrape_task >> save_json_task >> save_db_task