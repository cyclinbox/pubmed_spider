#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os,sys,json
import pandas as pd
import numpy  as np
import requests
import bs4
from bs4 import BeautifulSoup
import datetime,time
from http import HTTPStatus
# import libqwen,libernie
# import libpubmed
# import libgeturl


# In[3]:


# get pmid from article title.
def get_pmid_by_title(title):
    # param: string, article title
    # return: list, a list of pmids
    headers = {
        'Content-Type': 'application/json',
        'Accept'    : 'application/json',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    }

    url = f"https://pubmed.ncbi.nlm.nih.gov/?term='{title}'"
    req = requests.get(url,headers=headers)
    req.encoding = "utf-8"
    txt = req.text
    bs4obj = BeautifulSoup(txt,'lxml')
    # define a list for pmid storage.
    pmid_res_list = []
    # if searched multiple articles
    search_results = bs4obj.find_all("div",class_="search-results-chunk results-chunk")
    if(len(search_results)>0):
        search_results_chunk = bs4obj.find_all("div",class_="search-results-chunk results-chunk")[0]
        docsum_pmid_list = search_results_chunk.find_all("span",class_="docsum-pmid")
        pmid_res_list = []
        for i in range(len(docsum_pmid_list)):
            pmid = docsum_pmid_list[i].get_text()
            if(pmid not in pmid_res_list):
                pmid_res_list.append(pmid)
    # if searched single articles
    else:
        current_id_list = bs4obj.find_all("strong",class_="current-id")
        pmid_res_list = []
        for i in range(len(current_id_list)):
            pmid = current_id_list[i].get_text()
            if(pmid not in pmid_res_list):
                pmid_res_list.append(pmid)
    return pmid_res_list


# In[4]:


# get abstract, pmcid, full text
def get_bs4obj_by_pmid(pmid):
    url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    headers = {
        'Content-Type': 'application/json',
        'Accept'    : 'application/json',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    }
    req = requests.get(url,headers=headers)
    req.encoding = "utf-8"
    txt = req.text
    bs4obj = BeautifulSoup(txt,'lxml')
    return bs4obj


# In[5]:


# get abstract, pmcid, full text
def get_pmcid_by_bs4obj(bs4obj):
    # process bs4obj and extract pmcid
    pmcid_list = []
    all_ul_list=bs4obj.find_all("ul", class_=['identifiers'])
    for li in all_ul_list:
        all_link_list = li.find_all("a")
        if(len(all_link_list)>0):
            for link in all_link_list:
                attrs = link.attrs
                if("data-ga-action" in attrs):
                    if("PMCID" in attrs["data-ga-action"]):
                        #print(link.get_text())
                        pmcid = link.get_text().strip()
                        if(pmcid not in pmcid_list):
                            pmcid_list.append(pmcid)
                        break
    return pmcid_list


# In[6]:


# get abstract, pmcid, full text
def get_pmcid_by_pmid(pmid):
    bs4obj = get_bs4obj_by_pmid(pmid)
    pmcid_list = get_pmcid_by_bs4obj(bs4obj)
    return pmcid_list


# In[7]:


# get abstract, pmcid, full text
def get_abstract_by_bs4obj(bs4obj,plain_text=True):
    # process bs4obj and extract abstract
    header_text = ""
    abstract_text = ""
    try:
        main_chunk = bs4obj.find_all("main")[0]
        header_text= main_chunk.find_all("header")[0].get_text().strip()
        all_divs =  main_chunk.find_all("div")

        for div in all_divs:
            attrs = div.attrs
            if("id" in attrs):
                if("abstract" in attrs["id"]):
                    abstract_text = div.get_text().strip()
                    break
    except Exception as e:
        print(f"An error occurred in `get_abstract_by_pmid`: {e}")
        pass
    if(plain_text):
        return header_text+"\n## Abstract\n"+abstract_text
    else:
        return [header_text,abstract_text]
            
            


# In[8]:


# get abstract, pmcid, full text
def get_abstract_by_pmid(pmid,plain_text=True):
    bs4obj = get_bs4obj_by_pmid(pmid)
    return get_abstract_by_bs4obj(bs4obj,plain_text=plain_text)            


# In[9]:


# get abstract, pmcid, full text
def get_fulltext_by_pmcid(pmcid):
    #pmcid = "PMC8558904"
    url = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
    headers = {
        'Content-Type': 'application/json',
        'Accept'    : 'application/json',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    }
    req = requests.get(url,headers=headers)
    req.encoding = "utf-8"
    txt = req.text
    bs4obj = BeautifulSoup(txt,'lxml')
    #find main div with id="main-content"
    main_text = bs4obj.find_all("main")[0].get_text().strip()
    return main_text


# In[10]:


def get_and_save_text_by_title(title,output_dir):
    # param: string, article title
    # return: list, a list of pmids
    headers = {
        'Content-Type': 'application/json',
        'Accept'    : 'application/json',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    }
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term='{title}'"
    req = requests.get(url,headers=headers)
    req.encoding = "utf-8"
    txt = req.text
    bs4obj = BeautifulSoup(txt,'lxml')
    # define a list for pmid storage.
    pmid_res_list  = []
    pmcid_res_list = []
    # if searched multiple articles
    search_results = bs4obj.find_all("div",class_="search-results-chunk results-chunk")
    if(len(search_results)>0):
        search_results_chunk = bs4obj.find_all("div",class_="search-results-chunk results-chunk")[0]
        docsum_pmid_list = search_results_chunk.find_all("span",class_="docsum-pmid")
        pmid_res_list = []
        for i in range(len(docsum_pmid_list)):
            pmid = docsum_pmid_list[i].get_text()
            if(pmid not in pmid_res_list):
                pmid_res_list.append(pmid)
        # process pmid_list and save text
        for pmid in pmid_res_list:
            bs4obj1 = get_bs4obj_by_pmid(pmid)
            abstract_text = get_abstract_by_bs4obj(bs4obj1)
            pmcid = get_pmcid_by_bs4obj(bs4obj1)
            full_text = ""
            if(len(pmcid)>0):
                full_text = get_fulltext_by_pmcid(pmcid[0])
                with open(f"{output_dir}/autosave-{pmid}.txt",'w',encoding="utf-8") as f:
                    print(f"writing file: autosave-{pmid}.txt")
                    f.write(full_text)
            else:
                with open(f"{output_dir}/autosave-{pmid}.txt",'w',encoding="utf-8") as f:
                    print(f"writing file: autosave-{pmid}.txt")
                    f.write(abstract_text)
    # if searched single articles
    else:
        current_id_list = bs4obj.find_all("strong",class_="current-id")
        pmid_res_list = []
        for i in range(len(current_id_list)):
            pmid = current_id_list[i].get_text()
            if(pmid not in pmid_res_list):
                pmid_res_list.append(pmid)
        abstract_text = get_abstract_by_bs4obj(bs4obj)
        if(len(pmid_res_list)==0):
            pass
        else:
            pmid = pmid_res_list[0]
            pmcid = get_pmcid_by_bs4obj(bs4obj)
            full_text = ""
            if(len(pmcid)>0):
                full_text = get_fulltext_by_pmcid(pmcid[0])
                with open(f"{output_dir}/autosave-{pmid}.txt",'w',encoding="utf-8") as f:
                    print(f"writing file: autosave-{pmid}.txt")
                    f.write(full_text)
            else:
                with open(f"{output_dir}/autosave-{pmid}.txt",'w',encoding="utf-8") as f:
                    print(f"writing file: autosave-{pmid}.txt")
                    f.write(abstract_text)
    return pmid_res_list




# In[11]:


def run(zotero_export_csv_path, output_dir="saves"):
    print(f"input  csv file = {zotero_export_csv_path}")
    print(f"output dir path = {output_dir}")
    #os.system(f'mkdir -v "{output_dir}"')
    os.makedirs(output_dir,exist_ok=True)
    article_df = pd.read_csv(zotero_export_csv_path)
    #article_df.head(2)
    title_list = list(article_df["Title"])
    for i in range(len(title_list)):
        title = title_list[i]
        print(f"[{i}/{len(title_list)}]Processing article: `{title}`")
        get_and_save_text_by_title(title,output_dir)
        time.sleep(1) # sleep one second to avoid being banned by pubmed
    
    


# In[1]:


if(__name__=="__main__"):
    if(len(sys.argv)<2):
        print("Usage:\n\tpubmed_spider.py <zotero_export_csv> [output_dir]")
        sys.exit(0)
    zotero_export_csv_path = sys.argv[1]
    output_dir="saves"
    if(len(sys.argv)==3):
        output_dir = sys.argv[2]
    run(zotero_export_csv_path,output_dir)


