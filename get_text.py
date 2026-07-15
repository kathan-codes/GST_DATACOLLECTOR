import requests
from bs4 import BeautifulSoup
import re


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
}

url = "https://transportgstnumber.wordpress.com/transport-gst-number/"
gstin_results = []
with open("GST_NUMBER.txt",'w',encoding="utf-8") as f:
    f.write(f"===============GST NUMBER===============\n")
    f.close()
respons = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(respons.text,'html.parser')
soup_ = soup.prettify()
with open("DATA.txt","w",encoding="utf-8") as f:
    f.write(soup_)
spans  = soup.find_all("span", style="color:#000000;")

gstin_pattern = re.compile(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$')

for span in spans:
    text = span.get_text(strip=True).upper() # Convert to uppercase to match reliably
        
    # Only keep it if it perfectly matches the GSTIN structure
    if gstin_pattern.match(text):
        gstin_results.append(text)
        with open("GST_NUMBER.txt",'a',encoding="utf-8") as file:
            file.write(f"{text}\n") 

print(gstin_results)

