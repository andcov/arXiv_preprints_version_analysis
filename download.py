import requests
import time
import sys
import pandas as pd

# CSV with papers to download
csv_path = 'math_papers.csv'

# path to folder where the papers should be saved (!!! must add '/' at the end)
download_path = './papers/math/'

# number of papers to be downloaded
# !!! this does not reflect the actual number of papers that will be downloaded, as each paper has more than one version (at least 2 * download_size will be downloaded)
download_size = 4000

# a CSV with the papers that the script attempted to downloaded will be saved here
# this may be useful if the script fails and you are not sure what it was trying to download to begin with
to_download_csv_path = './papers/to_download_math_papers.csv'

# a CSV with the papers that were downloaded will be saved here
downloaded_csv_path = './papers/downloaded_math_papers.csv'

papers = pd.read_csv(csv_path, parse_dates = ['date'], dtype = {'id': str})

def download(paper):
    # download all versions of `paper`
    for i in range(1, paper['total_versions'] + 1):
        # some papers have '/' in their id
        # this does not work well with paths, so we replace '/' with '_'
        idx = paper['id'].replace('/', '_')
        
        # the papers are saved as a Pdf that may look like `1811.11745v1.pdf`
        name = idx + 'v' + str(i) + '.pdf'
        
        # the paper is requested from `export.arxiv.org` which is a domain dedicated to bots
        url = 'https://export.arxiv.org/pdf/' + name
        
        response = requests.get(url)
        with open(download_path + name, 'wb') as f:
            f.write(response.content)
            
        # a hard time limit between downloads is imposed so as to not put too much pressure on the Arxiv servers
        time.sleep(0.5) 
    downloaded_papers_id.append(paper['id'])
    
    # for debugging purposes
    if len(downloaded_papers_id) % 10 == 0:
        print('Downloaded: ', len(downloaded_papers_id))


downloaded_papers_id = []
to_download_papers = papers.drop_duplicates('id').sample(frac = 1).head(download_size)
to_download_papers.to_csv(to_download_csv_path, index=False)

# download papers
to_download_papers.apply(download, axis = 1)

papers.query('id in @downloaded_papers_id').reset_index(drop=True).to_csv(downloaded_csv_path, index=False)
