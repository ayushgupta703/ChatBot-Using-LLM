import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time

base_url = "https://thegloballearningacademy.com/"
visited = set()
chatbot_data = []


def is_valid_link(href):
    """Filter out non-page links and unwanted URLs"""
    excluded = ['#', 'tel:', 'mailto:', '.pdf', '.jpg']
    return not any(href.startswith(e) for e in excluded)


def extract_qa_pairs(soup):
    """Extract question-answer pairs from the page content."""
    qa_pairs = []

    for heading in soup.find_all(['h1', 'h2', 'h3']):
        question = heading.get_text(strip=True)
        answer = ""

        next_element = heading.find_next_sibling()
        while next_element and next_element.name not in ['h1', 'h2', 'h3']:
            answer += next_element.get_text(strip=True) + "\n"
            next_element = next_element.find_next_sibling()

        answer = answer.strip()
        if question and answer:
            qa_pairs.append({
                "question": question,
                "answer": answer
            })

    return qa_pairs


def scrape_page(url):
    try:
        if url in visited:
            return
        visited.add(url)

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'form']):
            element.decompose()

        qa_pairs = extract_qa_pairs(soup)
        if qa_pairs:
            chatbot_data.extend(qa_pairs)

        main_content = soup.find('main') or soup.find('article') or soup.body
        links = main_content.find_all('a', href=True) if main_content else []

        for link in links:
            href = link['href']
            if is_valid_link(href):
                full_url = urljoin(base_url, href)

                if full_url not in visited:
                    time.sleep(0.5)  # Add delay
                    try:
                        head_resp = requests.head(full_url, headers=headers, timeout=5)
                        if head_resp.status_code == 200:
                            scrape_page(full_url)
                    except:
                        continue

        time.sleep(1)

    except requests.HTTPError as e:
        print(f"Skipping {url} - Error: {e}")
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")


scrape_page(base_url)

with open('chatbot_data.json', 'w', encoding='utf-8') as f:
    json.dump(chatbot_data, f, indent=2, ensure_ascii=False)

print("Scraping completed. Data saved to chatbot_data.json")