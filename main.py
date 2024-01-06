import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_flipkart(query, num_pages=2):
    base_url = "https://www.flipkart.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    mobiles = []

    for page in range(1, num_pages + 1):
        search_url = f"{base_url}/search?q={query}&page={page}"
        
        try:
            # Step 1: Send a request to the Flipkart search page
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()  # Check if the request was successful

            # Step 2: Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Step 3: Extract relevant information
            for product in soup.find_all('div', {'class': '_1AtVbE'}):
                # Check if the name element is present
                name_element = product.find('div', {'class': '_4rR01T'})
                name = name_element.text.strip() if name_element else 'N/A'

                # Check if the price element is present
                price_element = product.find('div', {'class': '_30jeq3 _1_WHN1'})
                price = price_element.text.strip() if price_element else 'N/A'

                # Check if the ratings element is present
                ratings_element = product.find('div', {'class': '_3LWZlK'})
                ratings = ratings_element.text.strip() if ratings_element else 'N/A'
                
                specification_element = product.find('div', {'class': 'fMghEO'})
                # Initialize specifications to N/A
                storage, Display, Camera, Processor, Warranty = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
                
                if specification_element:
                    specs = specification_element.find_all('li', {'class': 'rgWa7D'})
                    for spec in specs:
                        text = spec.text.strip()
                        if 'GB' in text:
                            storage = text
                        elif 'Display' in text:
                            Display = text
                        elif 'Camera' in text:
                            Camera = text
                        elif 'Processor' in text:
                            Processor = text
                        elif 'Warranty' in text:
                            Warranty = text

                    # Check if any key field has "N/A" value, exclude such products
                    if 'N/A' not in (name, price, ratings, storage, Display, Camera, Processor, Warranty):
                        mobiles.append({
                            'Name': name,
                            'Price': price,
                            'Ratings': ratings,
                            'Storage' : storage,
                            'Display' : Display, 
                            'Camera' : Camera,
                            'Processor' : Processor, 
                            'Warranty': Warranty
                        })

            print(f"Page {page} scraped successfully.")
            time.sleep(3)

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")

    # Step 4: Store the extracted data in a CSV file
    csv_file_path = f'{query}_result.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Name', 'Price', 'Ratings', 'Storage', 'Display', 'Camera', 'Processor', 'Warranty']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(mobiles)

    print(f"Data has been successfully scraped and stored in {csv_file_path}")

if __name__ == "__main__":
    query = input("Enter the product you want to search for on Flipkart: ")
    num_pages = int(input("Enter the number of pages to scrape: "))
    scrape_flipkart(query, num_pages)
