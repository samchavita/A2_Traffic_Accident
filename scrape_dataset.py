import requests
from bs4 import BeautifulSoup
import os
import shutil

def download_files(urls, update_time, dir="./datasets/"):
    update_time = update_time.replace(":", "").replace(" ", "_")

    # verifying if datasets are up to date
    if not os.path.exists(dir):
        os.makedirs(dir)
    elif update_time in os.listdir(dir) and len(os.listdir( os.path.join(dir, update_time) )) == len(urls):
        print("datasets are up to date...\nall done.")
        return

    # downloading datasets
    os.makedirs( os.path.join(dir, update_time), exist_ok=True )
    try:
        print("downloading datasets...")
        i = 0

        for url in urls:
            i += 1
            filename=url.split("/")[-2]
            
            print( f'{i}: ', end="\t")
            # print( filename )
            # print( url )

            response = requests.get(url, verify=False)
            with  open(os.path.join(dir, update_time, filename + ".zip" ),'wb') as f:
                f.write(response.content)
                print(f'downloaded {filename}')

        print("downloading complete!")

        # update latest folder
        if os.path.exists( os.path.join(dir, "latest") ):
            shutil.rmtree( os.path.join(dir, "latest") )
        shutil.copytree( os.path.join(dir, update_time), os.path.join(dir, "latest") )

    except Exception as e:
        print("error dowloading datasets:\n", e)
    
        


def main():
    url = "https://data.gov.tw/en/datasets/13139"
    page = requests.get(url)
    soup =  BeautifulSoup(page.content, 'html.parser')
    rows =  soup.find_all("div", class_="table-row")
    urls = []
    update_time = ""

    # get urls of datasets and update time
    for row in rows:
        if len(url) and update_time:
            break

        # find download links
        if ( urls == [] and row.find_all("strong")[0].get_text() == "Resources download link" ):
            urls = [ link.get("href") for link in row.find_all("a") ]
        
        # find last update time
        elif ( not update_time and row.find_all("strong")[0].get_text() == "Updated time" ):
            
            update_time = row.find_all("div")[-1].get_text().strip()

    # download datasets
    download_files(urls, update_time)

if __name__  == "__main__":
    main()