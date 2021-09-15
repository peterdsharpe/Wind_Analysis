import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from tqdm import tqdm

this_directory = Path(__file__).parent

soup = BeautifulSoup(
    requests.get(
        "https://espoarchive.nasa.gov/archive/browse/atom/DC8/MMS-20Hz"
    ).text,
    features="lxml",
)

all_links = [
    link.get('href')
    for link in soup.find_all('a')
]

links_to_download = []

for link in all_links:
    if isinstance(link, str):
        if link[-3:] == "ict":
            if "download" in link:
                links_to_download.append(link)

links_to_download = [
    "https://espoarchive.nasa.gov" + link
    for link in links_to_download
]

for link in tqdm(links_to_download, desc="File Download", unit="file"):
    data = requests.get(link).text
    filename = link.split("/")[-1]
    with open(this_directory / "data" / filename, "w+") as f:
        f.write(data)


