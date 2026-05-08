import requests
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
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

for msg in messages[-20:][::-1]:

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
        post_link = link_tag["href"]

    iran_time = datetime.now(ZoneInfo("Asia/Tehran"))
    formatted = iran_time.strftime("%Y-%m-%d %H:%M:%S")
    
    post_html = f"""
######🔵  Updated at: {formatted}

{image_html}

{text}

[View Post]({post_link})

---

"""

    posts_html.append(post_html)

posts_content = "\n".join(posts_html)

#debug
print("POSTS CONTENT LENGTH:", len(posts_content))

# UPDATE README
start = "<!-- POSTS_START -->"
end = "<!-- POSTS_END -->"

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Case 1: markers exist → replace normally
if start in content and end in content:
    before = content.split(start)[0]
    after = content.split(end)[1]

    new_content = (
        before
        + start + "\n"
        + posts_content + "\n"
        + end
        + after
    )

# Case 2: markers missing → auto-create section
else:
    new_content = content.strip() + f"""

{start}
{posts_content}
{end}
"""

# Write back
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)

print("README updated (auto-safe mode).")
