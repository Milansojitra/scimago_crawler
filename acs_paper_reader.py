import sys
import requests
from bs4 import BeautifulSoup
import traceback
from icecream import ic 


def get_paper_info(page_id):

    page_url = f"https://www.scimagojr.com/journalsearch.php?q={page_id}&tip=sid&clean=0"
    out = dict()

    try:
        html_text = requests.get(page_url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        data =soup.find("div", {"class":"journaldescription"})
        out['title'] = data.find("h1").text.strip()

        for d in soup.find("div", {"class":"journalgrid"}).findAll("div"):
            try:
                h_text = d.find("h2")
                if h_text:
                    if "index" in h_text.text.lower():
                        out['h_index'] = d.find("p").text
                    elif "country" in h_text.text.lower():
                        out['country'] = d.find("p").text.strip().split("\n")[0]
                    elif "issn" in h_text.text.lower():
                        out['issn'] = d.find("p").text.replace(",", "-")

                    elif "information" in h_text.text.lower():
                        for p_tag in d.findAll("p"):
                            if "homepage" in p_tag.text.lower():
                                out['homepage_url'] = p_tag.find("a").get("href")
                            if "how" in p_tag.text.lower() and "publish" in p_tag.text.lower():
                                out['guideline_url'] = p_tag.find("a").get("href")
            except:
                print(traceback.format_exc())
    except:
        print(traceback.format_exc())
        sys.exit()
    return out


