import requests
import time
import sys
import pandas as pd

mode = "math" # or "cs"
download_path = "./papers"

if mode == "math":
    csv_name = "math_papers.csv"
    folder_name = download_path + "/math/"
elif mode == "cs":
    csv_name = "cs_papers.csv"
    folder_name = download_path + "/cs/"
else:
    print("Available args are `math` or `cs`")
    quit()

papers = pd.read_csv(csv_name, parse_dates = ["date"], low_memory=False)

def download(x):
    for i in range(1, x["versions"] + 1):
        idx = x["id"].replace("/", "_")
        name = idx + "v" + str(i) + ".pdf"
        url = "https://export.arxiv.org/pdf/" + name
        response = requests.get(url)
        with open(folder_name + name, 'wb') as f:
            f.write(response.content)
        print("Downloaded " + name)
        time.sleep(1)
    print()

papers.loc[papers["versions"] <= 4].sample(frac=1).head(50).apply(download, axis = 1)
