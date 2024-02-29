import script_function
import os
import requests
from bs4 import BeautifulSoup

# Scraper tous les livres et sauvegarder les données par catégorie
def scrape_all_books(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        categories = soup.find('ul', class_='nav-list').find_all('a')
        for category in categories:
            category_url = url.rsplit('/', 1)[0] + '/' + category['href']
            category_name = category.text.strip()
            if category_name == "Books":
                print("Skipping 'Books' category...")
                continue
            print(f"Scraping category: {category_name}")
            category_books_info = script_function.scrape_category_books(category_url)
            script_function.save_to_csv(category_books_info, category_name, "all_books_csv")
            print(f"Category {category_name} scraped and saved successfully.")
    else:
        print("Erreur lors de la requête HTTP :", response.status_code)


def main():
    base_url = 'https://books.toscrape.com/'
    os.makedirs('all_books_csv', exist_ok=True)
    scrape_all_books(base_url)

if __name__ == "__main__":
    main()