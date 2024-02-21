import requests
from bs4 import BeautifulSoup
import csv

def scrape_books_in_category(category_url):
    all_books_info = []
    page_number = 1
    while True:
        response = requests.get(f"{category_url}/page-{page_number}.html")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            books = soup.find_all('h3')
            if len(books) == 0:
                break  # Pas de livres sur cette page, donc fin de la pagination
            for book in books:
                book_link = book.find('a')['href']
                book_info = scrape_book_info(f"{category_url}/{book_link}")
                if book_info:
                    all_books_info.append(book_info)
            page_number += 1
        else:
            print("Erreur lors de la requête HTTP :", response.status_code)
            break
    return all_books_info


def scrape_book_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extraire les informations nécessaires
        product_page_url = url
        title = soup.find('h1').text.strip()
        
        # Chercher UPC
        upc_element = soup.find('th', text='UPC')
        upc = upc_element.find_next('td').text.strip() if upc_element else None
        
        price_including_tax = soup.find('p', class_='price_color').text.strip()
        price_excluding_tax = soup.find_all('td')[2].text.strip()
        availability = soup.find('p', class_='instock availability').text.strip()
        number_available = ''.join(filter(str.isdigit, availability))  # Extraire le nombre disponible
        product_description = soup.find('meta', attrs={'name': 'description'})['content'].strip()
        category = soup.find('ul', class_='breadcrumb').find_all('a')[-1].text.strip()
        review_rating = soup.find('p', class_='star-rating')['class'][1]
        image_url = soup.find('div', class_='item active').find('img')['src'].replace('../..', 'https://books.toscrape.com')
        
        return {
            'product_page_url': product_page_url,
            'universal_product_code (upc)': upc,
            'title': title,
            'price_including_tax': price_including_tax,
            'price_excluding_tax': price_excluding_tax,
            'number_available': number_available,
            'product_description': product_description,
            'category': category,
            'review_rating': review_rating,
            'image_url': image_url
        }
    else:
        print("Erreur lors de la requête HTTP :", response.status_code)
        return None

def clean_data(book_info):
    cleaned_data = []
    for book in book_info:
        # Nettoyer le prix
        book['price_including_tax'] = book['price_including_tax'].replace('£', '')
        book['price_excluding_tax'] = book['price_excluding_tax'].replace('£', '')
        
        # Convertir l'évaluation en numérique
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        book['review_rating'] = rating_map.get(book['review_rating'])
        
        cleaned_data.append(book)
    
    return cleaned_data

def save_to_csv(data, filename='books_info.csv'):
    cleaned_data = clean_data(data)
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cleaned_data[0].keys())
        writer.writeheader()
        writer.writerows(cleaned_data)