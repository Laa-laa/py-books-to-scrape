import script_function

def main():
    category_url = "https://books.toscrape.com/catalogue/category/books/mystery_3"
    all_books_info = script_function.scrape_books_in_category(category_url)
    if all_books_info:
        script_function.save_to_csv(all_books_info)
        print("Les informations ont été sauvegardées avec succès dans le fichier CSV.")
    else:
        print("Impossible de récupérer les informations des livres de cette catégorie.")

if __name__ == "__main__":
    main()