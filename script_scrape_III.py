import script_function
import os

def main():
    base_url = 'https://books.toscrape.com/'
    os.makedirs('all_books_csv', exist_ok=True)
    script_function.scrape_all_books(base_url)

if __name__ == "__main__":
    main()