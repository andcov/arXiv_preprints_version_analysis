import requests
import time
import sys
import pandas as pd

csv_path = "phys_papers.csv"
download_path = "/mnt/volume_nyc1_01/phys/"
downloaded_csv_path= "../downloaded_phys_papers.csv"


papers = pd.read_csv(csv_path, parse_dates = ["date"], dtype = {'id': str}, low_memory=False)

def download(paper):
    for i in range(1, paper["total_versions"] + 1):
        idx = paper["id"].replace("/", "_")
        name = idx + "v" + str(i) + ".pdf"
        url = "https://export.arxiv.org/pdf/" + name
        response = requests.get(url)
        with open(download_path + name, 'wb') as f:
            f.write(response.content)
        time.sleep(0.2)

    downloaded_papers_id.append(paper["id"])
    if len(downloaded_papers_id) % 10 == 0:
        print("Downloaded: ", len(downloaded_papers_id))


downloaded_papers_id = []
to_download_papers = papers.drop_duplicates("id").sample(frac = 1).head(4000)
to_download_papers.to_csv("to_download_phys.csv", index=False)
to_download_papers.apply(download, axis = 1)

papers.query("id in @downloaded_papers_id").reset_index(drop=True).to_csv(save_csv_path, index=False)
