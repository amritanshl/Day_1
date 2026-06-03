import requests

target_url = f"https://www.oxitsolutions.co.uk/blog/http-status-code-cheat-sheet-infographic"
print("Sending programmatic GET request...")

response = requests.get(target_url)

if response.status_code == 200:
    print("Success ! Webpage downloaded")
    
    raw_html = response.text
    with open("my_file.html", "w", encoding="utf-8") as file:
        file.write(raw_html)
    print("Saved file as 'wikipedia.html'. Go double-click it!")
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")