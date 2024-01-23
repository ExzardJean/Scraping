import requests
from bs4 import BeautifulSoup
import csv

class NouvellisteScraper:
    BASE_URL = 'https://lenouvelliste.com/'

    def __init__(self):
        pass

    @staticmethod
    def recuperer(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def Extrait(soup):
        article_classes = ['lnv-featured-article', 'lnv-featured-article-sm']
        article_divs = [soup.find_all('div', class_=class_) for class_ in article_classes]
        articles = [article for sublist in article_divs for article in sublist]

        data_list = []

        for article in articles:
            title = article.find('h1').text.strip()
            link = NouvellisteScraper.BASE_URL + article.find('a')['href'] if article.find('a') else None
            image = article.find('img')['src'] if article.find('img') else None
            description = article.find('p').text

            data_list.append([title, link, image, description])

        return data_list

    @staticmethod
    def Etudiant(data_list, csv_filename='Nouvelliste.csv'):
        header = ['Title', 'Link', 'Image', 'Description']
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(header)
            csv_writer.writerows(data_list)

    def scrape_lenouvelliste(self):
        url = NouvellisteScraper.BASE_URL
        page_content = NouvellisteScraper.recuperer(url)

        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            data_list = NouvellisteScraper.Extrait(soup)
            NouvellisteScraper.Etudiant(data_list)
            print("Web scraping completed successfully.")

if __name__ == "__main__":
    scraper = NouvellisteScraper()
    scraper.scrape_lenouvelliste()
