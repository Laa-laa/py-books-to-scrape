import script_function
import os

def main():
    url = "https://books.toscrape.com/catalogue/dune-dune-1_151/index.html"
    book_info = script_function.scrape_book_info(url)
    if book_info:
        os.makedirs('one_book', exist_ok=True)
        script_function.save_to_csv([book_info], "one_book","one_book")
        print("Les informations ont été sauvegardées avec succès dans le fichier CSV.")
    else:
        print("Impossible de récupérer les informations du livre.")

if __name__ == "__main__":
    main()