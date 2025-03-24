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

    # Extract headings (h1, h2, h3) and their following content
    for heading in soup.find_all(['h1', 'h2', 'h3']):
        question = heading.get_text(strip=True)
        answer = ""

        # Find the next sibling elements (content after the heading)
        next_element = heading.find_next_sibling()
        while next_element and next_element.name not in ['h1', 'h2', 'h3']:
            answer += next_element.get_text(strip=True) + "\n"
            next_element = next_element.find_next_sibling()

        # Clean up the answer
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

        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'form']):
            element.decompose()

        # Extract Q&A pairs
        qa_pairs = extract_qa_pairs(soup)
        if qa_pairs:
            chatbot_data.extend(qa_pairs)

        # Find MAIN CONTENT AREA only (skip navigation)
        main_content = soup.find('main') or soup.find('article') or soup.body
        links = main_content.find_all('a', href=True) if main_content else []

        # Process links with rate limiting
        for link in links:
            href = link['href']
            if is_valid_link(href):
                full_url = urljoin(base_url, href)

                # Verify URL exists before adding to children
                if full_url not in visited:
                    time.sleep(0.5)  # Add delay
                    try:
                        head_resp = requests.head(full_url, headers=headers, timeout=5)
                        if head_resp.status_code == 200:
                            scrape_page(full_url)
                    except:
                        continue

        time.sleep(1)  # Respectful delay

    except requests.HTTPError as e:
        print(f"Skipping {url} - Error: {e}")
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")


# Start scraping
scrape_page(base_url)

# Save JSON
with open('chatbot_data.json', 'w', encoding='utf-8') as f:
    json.dump(chatbot_data, f, indent=2, ensure_ascii=False)

print("Scraping completed. Data saved to chatbot_data.json")