##Code to scrape the CP sheet of striver and place it in a .csv file topic-wise
import requests
import argparse
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_html_content(url):
    r = requests.get(url)
    return r.text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, help="Link to the CP sheet",\
    default="https://takeuforward.org/interview-experience/strivers-cp-sheet/?utm_source=youtube&utm_medium=striver&utm_campaign=yt_video")
    parser.add_argument("--dest_path", type=str, help="Path to excel sheet",\
    default="problems.xlsx")
    args = parser.parse_args()

    html_content = get_html_content(args.url)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    csv_file_names = []
    problem_links = []

    for detail in soup.find_all('details'):
        children = detail.children
        flag = False
        for child in children:
            if child.name=="ol":
                flag = True
                break

        if flag==True:
            children = detail.children
            problems = []
            for child in children:
                if child.name=="summary":
                    title = str(child.text)
                    normal_title = "".join(ch for ch in title if ch.isalnum())
                    csv_file_names.append(title)
                if child.name=="ol":
                    problems_li = child.children
                    for problem in problems_li:
                        link = str(problem.text)
                        if link.startswith("https"):
                            problems.append(link)

            problem_links.append(problems)

    writer = pd.ExcelWriter(args.dest_path, engine='xlsxwriter')
    
    for i, file_name in enumerate(csv_file_names):
        df = pd.DataFrame({'Problem Link': problem_links[i]})
        df.to_excel(writer, sheet_name=re.sub('[^a-zA-Z \n\.]', '', file_name)[:31])

    writer.close()

if __name__=="__main__":
    main()