import requests
import pandas as pd
from bs4 import BeautifulSoup


def scrape_news_site():
    base_url = "https://www.bbc.com"
    sports_url = f"{base_url}/sport"

    response = requests.get(sports_url)
    response

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
    list_of_links = []
    raw_link = soup.find_all("a")
    for link in raw_link:
        href = link.get("href")
        if href and "/articles/" in href and "#comments" not in href:
            full_url = f"{base_url}{href}"
            list_of_links.append(full_url)

    news_list = []
    for link in list_of_links:
        res = requests.get(link)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html.parser")
            h1_tag = soup.find("h1", id="main-heading")

            if not h1_tag:
                continue
            span_tag = h1_tag.find("span")

            if not span_tag:
                continue
            news_title = span_tag.get_text()

            author_div = soup.find(
                "div", class_="ssrcss-68pt20-Text-TextContributorName"
            )
            author_name = author_div.get_text() if author_div else "Author not found"
            metadata = soup.find("div", class_="ssrcss-m5j4pi-MetadataContent")

            if not metadata:
                continue
            date_ = metadata.find("time")

            if not date_:
                continue
            datetime = date_["datetime"]

            final_content = ""
            content_divs = soup.find_all(
                "div", class_="ssrcss-7uxr49-RichTextContainer"
            )
            for div in content_divs:
                p_tags = div.find_all("p")
                for p in p_tags:
                    final_content += p.text + "\n"
            news = {
                "title": news_title,
                "author": author_name,
                "date": datetime,
                "url": link,
                "content": final_content,
            }
            news_list.append(news)

    nlp_df = pd.DataFrame(news_list)
    print(nlp_df.head())
    return nlp_df
