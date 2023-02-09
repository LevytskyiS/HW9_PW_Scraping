import requests
import json
from bs4 import BeautifulSoup


url = "http://quotes.toscrape.com"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}


class GetAllPages:
    @classmethod
    def get_all_pages(self):

        all_pages = []
        page = 1

        for page in range(1, 11):
            current_url = url + f"/page/{page}/"
            request = requests.get(current_url, headers=header)

            if request.status_code == 200:
                print(
                    f"Page '{page}' was checked. The status code is {request.status_code}"
                )
                all_pages.append(request)

        return all_pages

    @classmethod
    def check_collected_links(self, links):

        checked_links = []

        for link in set(links):
            request = requests.get(link, headers=header)

            if request.status_code == 200:
                checked_links.append(request)
                print(
                    f"The link '{link}' was checked. The status code is {request.status_code}"
                )

        return checked_links


class GetData:
    @classmethod
    def get_quotes(self, pages):

        result = []
        authors_links = []

        for page in pages:

            soup = BeautifulSoup(page.text, "lxml")
            quote_card = soup.find_all("div", class_="quote")

            for data in quote_card:

                tags_html = data.find("div", class_="tags").find_all("a", class_="tag")

                tags = []
                for tag in tags_html:
                    tags.append(tag.text)

                author = data.find("small", class_="author").text
                author_link = url + data.find("a").get("href")
                authors_links.append(author_link)

                quote = data.find("span", class_="text").text

                result.append({"tags": tags, "author": author, "quote": quote})

        with open("quotes_hw.json", "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

        return authors_links

    @classmethod
    def get_author_info(self, sources):

        result = []

        for source in sources:

            soup = BeautifulSoup(source.text, "lxml")
            author_card = soup.find_all("div", class_="author-details")

            for data in author_card:

                fullname = data.find("h3", class_="author-title").text.strip()
                born_date = data.find("span", class_="author-born-date").text
                born_location = data.find("span", class_="author-born-location").text
                description = data.find("div", class_="author-description").text.strip()

                result.append(
                    {
                        "fullname": fullname,
                        "born_date": born_date,
                        "born_location": born_location,
                        "description": description,
                    }
                )

        with open("authors_hw.json", "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

        print("Done")

        return "Done"


if __name__ == "__main__":
    pages = GetAllPages.get_all_pages()
    links_to_author = GetData.get_quotes(pages)
    authors_sources = GetAllPages.check_collected_links(links_to_author)
    get_data_from_authors = GetData.get_author_info(authors_sources)
