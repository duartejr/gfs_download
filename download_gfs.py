#%%
import os
import requests
from bs4 import BeautifulSoup
from clint.textui import progress

def download_gfs(links):
    with open(links) as file:
        for link in file:
            print('Starting a new download:')
            link = link.strip("\n")
            print(f'-> {link}')
            page = requests.get(link).text
            soup = BeautifulSoup(page, 'html.parser')
            link_download = [link + node.get('href') for node in soup.find_all('a')\
                            if node.get('href').endswith('.tar')][0]
            print(f'URL: {link_download}')
            path = link_download.split('/')[-1]
            print(f'Output file: {path}')
            r = requests.get(link_download, path, stream=True)
            with open(path, 'wb') as f:
                total_length = int(r.headers.get('content-length'))
                for chunk in progress.bar(r.iter_content(chunk_size=1_048_576), 
                                          expected_size=(total_length/1_048_576) + 1): 
                    if chunk:
                        f.write(chunk)
                        f.flush()
            print(f'Done ----> {link_download}')
            print("="*60)


if __name__ == "__main__":
    output_dir = 'source_to/GFS'
    os.chdir(output_dir)
    links = f'source_to/gfs_download_urls.txt'
    download_gfs(links)