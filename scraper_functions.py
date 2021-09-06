# %%
import requests
import os 
import urllib
from bs4 import BeautifulSoup
import re
import math
# %%
def load_indeed_jobs_div(job_title, location, job_type, start_page="", radius=25):
    getVars = {'q' : job_title, 'l' : location, "radius" : radius, "jt" : job_type, "fromage" : "any", "limit" : 50, "psf" : "advsrch", "from" : "advancedsearch", 'sort' : 'date', "start" : start_page}
    url = ('https://dk.indeed.com/jobs?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def find_number_of_pages(job_soup):
    page_nr = job_soup.find("div", id="searchCountPages")
    page_nr = re.findall(r"(\d+) jobs", str(page_nr))[0]
    number_of_pages = math.ceil(int(page_nr) / 50)
    return number_of_pages

# %%
job_title = '"data science"'
location = "København"
job_type = "fulltime"
job_soup = load_indeed_jobs_div(job_title, location, job_type)
# %%
number_of_pages = find_number_of_pages(job_soup)
# %%

job_links = []

for overview_page in range(number_of_pages):
    start_page = (overview_page) * 50
    print(start_page)
    job_soup = load_indeed_jobs_div(job_title, location, job_type, start_page)
    job_elems = job_soup.find_all("a", id=re.compile("job_"))
    for job in job_elems:
        job_links.append(re.findall(r"data-jk=\"(.[\w]+)",str(job))[0])

job_links = set(job_links)

# %%
def get_job_view(jobkey):
    getVars = {'jk' : jobkey, "vjs" : "3"}
    url = ('https://dk.indeed.com/viewjob?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def extract_job_title_indeed(job_elem):
    title_elem = job_elem.find("div", class_="jobsearch-JobInfoHeader-title-container")
    title = title_elem.text.strip()
    return title

def extract_company_indeed(job_elem):
    company_elem = job_elem.find('div', class_='icl-u-lg-mr--sm icl-u-xs-mr--xs')
    company = company_elem.text.strip()
    return company

def extract_date_indeed(job_elem):
    date_elem = job_elem.find('div', class_='jobsearch-JobMetadataFooter')
    date = re.findall(r"(\d+) dage siden", str(date_elem))
    return date

def extract_job_link_indeed(job_elem):
    link_elem = job_elem.find('div', id='originalJobLinkContainer')
    link = link_elem.find(href=True)["href"]
    return link


# %%
title = []
company = []
date = []
description = []
application_link = []
i = 0

for job_link in job_links:
    job_elem = get_job_view(job_link)
    title.append(extract_job_title_indeed(job_elem))
    company.append(extract_company_indeed(job_elem))
    application_link.append(extract_job_link_indeed(job_elem))
    date.append(extract_date_indeed(job_elem))
    i += 1
    print(i)
    
# %%

# Set up dockerization
# Set up github actions regualr run
# Set up bash script for running
# Set up data cleaning
# Set up analysis - content?
# Set up overview of jobs
# Set up visualization? - content?
# Set up API? - content?