"""
ISOM3400 Individual Assignment - Wikipedia Article Extractor
Name: Yonathan Aklilu Kidanemariam
Student ID: 21139206
Email: yak@connect.ust.hk

Terminal: python wikipedia_extractor.py (or python app.py)
Website: streamlit run app.py
"""

from datetime import datetime
from pathlib import Path
from urllib.parse import quote
import re

import requests
from bs4 import BeautifulSoup


# Store an article and collect its top-level sections in reading order.
class WikipediaArticle:
    def __init__(self, topic):
        self.url = "https://en.wikipedia.org/wiki/" + quote(topic.replace(" ", "_"), safe="")
        self.title = topic
        self.sections = {}

    # Download and parse headings, paragraphs, lists, and tables.
    def fetch(self):
        response = requests.get(
            self.url,
            headers={"User-Agent": "ISOM3400StudentExtractor/1.0 (educational project; yak@connect.ust.hk)"},
            timeout=20,
        )
        if response.status_code == 404:
            raise ValueError("Article not found. Please try another topic.")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1", id="firstHeading")
        article_body = soup.find("div", id="mw-content-text")
        if article_body is None:
            article_body = soup
        content = article_body.find("div", class_="mw-parser-output")
        if title is None or content is None:
            raise ValueError("The article layout was not recognised. Please try another topic.")
        self.title = title.get_text(" ", strip=True)
        self.url = response.url
        for unwanted in content.select("sup.reference, .mw-editsection, .noprint"):
            unwanted.decompose()

        section = "Introduction"
        self.sections = {section: []}
        for element in content.find_all(["h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "table"]):
            # Process lists and tables as whole blocks to avoid repeating their text.
            if element.find_parent(["table", "ul", "ol"]) is not None:
                continue
            text = element.get_text(" ", strip=True)
            if not text:
                continue
            if element.name == "h2":
                section = text
                self.sections[section] = []
            elif element.name in ["h3", "h4", "h5", "h6"]:
                self.sections[section].append("\n" + text)
            elif element.name in ["ul", "ol"]:
                for number, item in enumerate(element.find_all("li"), 1):
                    marker = str(number) + ". " if element.name == "ol" else "- "
                    self.sections[section].append(marker + item.get_text(" ", strip=True))
            elif element.name == "table":
                for row in element.find_all("tr"):
                    cells = row.find_all(["th", "td"], recursive=False)
                    if cells:
                        self.sections[section].append(" | ".join(cell.get_text(" ", strip=True) for cell in cells))
            else:
                self.sections[section].append(text)
        if not any(self.sections.values()):
            raise ValueError("No readable sections were found. Please try another article.")

    # Add attribution and combine the selected sections into a readable extract.
    def extract(self, selected):
        text = [self.title, "Source: " + self.url,
                "Extracted: " + datetime.now().astimezone().isoformat(timespec="seconds"),
                "Licence: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)"]
        titles = list(self.sections)
        for number in selected:
            title = titles[number - 1]
            text.extend(["", title, "=" * len(title)])
            text.extend(self.sections[title])
        return "\n\n".join(text) + "\n"


# Accept numbers, comma-separated selections, ranges, or all; reject invalid input.
def select_sections(answer, count):
    if answer.strip().lower() == "all":
        return list(range(1, count + 1))
    selected = []
    for part in answer.split(","):
        part = part.strip()
        if not re.fullmatch(r"[0-9]+(?:\s*-\s*[0-9]+)?", part):
            raise ValueError("Use numbers, commas, ranges (such as 2-4), or all.")
        numbers = part.split("-")
        start = int(numbers[0])
        end = int(numbers[-1])
        if start < 1 or end > count or start > end:
            raise ValueError(f"Choose numbers between 1 and {count}, with ranges in ascending order.")
        for number in range(start, end + 1):
            if number not in selected:
                selected.append(number)
    return selected


# Save with a numbered filename when necessary, without overwriting existing files.
def save_extract(title, text):
    name = re.sub(r"[^\w -]", "", title).strip()[:100] or "Wikipedia_article"
    path = Path(name + ".txt")
    number = 1
    while True:
        try:
            with path.open("x", encoding="utf-8") as file:
                file.write(text)
            return path
        except FileExistsError:
            path = Path(f"{name}_{number}.txt")
            number += 1


# Run the required console interface with retry prompts and a graceful exit.
def main():
    print("Welcome to the Wikipedia Article Extractor!")
    print("Enter an article topic, choose sections, and save them to a text file.")
    print("Use numbers, commas, ranges, or all. Enter q at any prompt to exit.")
    try:
        while True:
            topic = input("\nWikipedia topic: ").strip()
            if topic.lower() == "q":
                break
            if not topic:
                print("Please enter a topic.")
                continue
            article = WikipediaArticle(topic)
            try:
                article.fetch()
            except (requests.RequestException, ValueError) as error:
                print("Could not load the article:", error)
                continue
            except Exception as error:
                print("Unexpected problem reading the article:", error)
                continue
            print("\n" + article.title)
            for number, title in enumerate(article.sections, 1):
                print(f"{number}. {title}")
            while True:
                answer = input("Sections (example: 1,3-5 or all): ").strip()
                if answer.lower() == "q":
                    print("Goodbye!")
                    return
                try:
                    selected = select_sections(answer, len(article.sections))
                    text = article.extract(selected)
                except ValueError as error:
                    print(error)
                    continue
                try:
                    path = save_extract(article.title, text)
                    print("Saved to:", path.resolve())
                    break
                except OSError as error:
                    print("Could not save the file:", error)
                    print("Check folder permissions or available space, then try again.")
    except (KeyboardInterrupt, EOFError):
        pass
    print("Goodbye!")


# Show the same extractor on Streamlit, using a download instead of a server-side file.
def website():
    st.title("Wikipedia Article Extractor")
    st.write("Search for an article, choose sections, and download a text extract.")
    topic = st.text_input("Wikipedia topic", placeholder="For example: Python (programming language)")
    if st.button("Find article"):
        st.session_state.pop("article", None)
        if not topic.strip():
            st.error("Please enter a topic.")
        else:
            try:
                article = WikipediaArticle(topic.strip())
                article.fetch()
                st.session_state.article = article
            except Exception as error:
                st.error(f"Could not load the article: {error}")
    if "article" in st.session_state:
        article = st.session_state.article
        st.header(article.title)
        for number, title in enumerate(article.sections, 1):
            st.write(f"{number}. {title}")
        answer = st.text_input("Sections (example: 1,3-5 or all)", value="all")
        try:
            selected = select_sections(answer, len(article.sections))
            text = article.extract(selected)
            st.text_area("Extract preview", text, height=300)
            filename = re.sub(r"[^\w -]", "", article.title).strip()[:100] or "Wikipedia_article"
            st.download_button("Download text file", text, file_name=filename + ".txt", mime="text/plain")
        except ValueError as error:
            st.error(str(error))


# Streamlit is optional; ordinary Python runs the required console interface.
if __name__ == "__main__":
    try:
        import streamlit as st
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        in_streamlit = get_script_run_ctx(suppress_warning=True) is not None
    except ImportError:
        in_streamlit = False
    if in_streamlit:
        website()
    else:
        main()
