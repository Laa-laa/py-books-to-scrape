import script_function
import os

def main():
    category_url = 'https://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
    all_books_info = script_function.scrape_category_books(category_url)
    if all_books_info:
        os.makedirs('book_category', exist_ok=True)
        script_function.save_to_csv(all_books_info,"book_category","book_category")
        print("Les informations ont été sauvegardées avec succès dans le fichier CSV.")
    else:
        print("Impossible de récupérer les informations des livres de cette catégorie.")

if __name__ == "__main__":
    main()