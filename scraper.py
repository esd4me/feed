import requests
from bs4 import BeautifulSoup
import re

CHANNEL = "VahidOnline"

url = f"https://t.me/s/{CHANNEL}?before=0"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(url, headers=headers).text

soup = BeautifulSoup(html, "lxml")

messages = soup.find_all("div", class_="tgme_widget_message_wrap")
#debug
#print(len(messages))
#print(html[:1000])

posts_html = []

for msg in messages[-10:][::-1]:

    # TEXT
    text_div = msg.find("div", class_="tgme_widget_message_text")

    text = ""
    if text_div:
        text = text_div.get_text("\n", strip=True)

    # IMAGE
    image_html = ""

    photo = msg.find("a", class_="tgme_widget_message_photo_wrap")

    if photo:
        style = photo.get("style", "")

        match = re.search(r"url\('(.*?)'\)", style)

        if match:
            img_url = match.group(1)
            image_html = f'<img src="{img_url}" width="400"><br>'

    # POST LINK
    link_tag = msg.find("a", class_="tgme_widget_message_date")

    post_link = ""
    if link_tag:
        post_link = "https://t.me" + link_tag["href"]

    post_html = f"""
## Telegram Post

{image_html}

{text}

[View Post]({post_link})

---

"""

    posts_html.append(post_html)

posts_content = "\n".join(posts_html)
print("POSTS CONTENT LENGTH:", len(posts_content))

# UPDATE README
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

pattern = r"<!-- POSTS_START -->(.*?)<!-- POSTS_END -->"

replacement = f"""<!-- POSTS_START -->
{posts_content}
<!-- POSTS_END -->"""

updated = re.sub(pattern, replacement, readme, flags=re.S)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)

print("README updated.")
