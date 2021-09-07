# %%
import requests
import os 
import urllib
from bs4 import BeautifulSoup
import re
import math
import pandas as pd
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


def get_job_view(jobkey, proxies):
    getVars = {'jk' : jobkey, "vjs" : "3"}
    url = ('https://dk.indeed.com/viewjob?' + urllib.parse.urlencode(getVars))
    page = requests.get(url, proxies=proxies)
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

def extract_description_indeed(job_elem):
    description_elem = job_elem.find('div', id='jobDescriptionText')
    description = description_elem.text.strip()
    return description


def scrape_indeed(job_title, location, job_type, proxies): # should be class?
    job_soup = load_indeed_jobs_div(job_title, location, job_type)
    number_of_pages = find_number_of_pages(job_soup)
    job_links = []

    for overview_page in range(number_of_pages):
        start_page = (overview_page) * 50
        print(start_page)
        job_soup = load_indeed_jobs_div(job_title, location, job_type, start_page)
        job_elems = job_soup.find_all("a", id=re.compile("job_"))
        for job in job_elems:
            job_links.append(re.findall(r"data-jk=\"(.[\w]+)",str(job))[0])

    job_links = set(job_links)

    title = []
    company = []
    date = []
    description = []
    application_link = []
    i = 0

    for job_link in job_links:
        job_elem = get_job_view(job_link, proxies)
        title.append(extract_job_title_indeed(job_elem))
        company.append(extract_company_indeed(job_elem))
        application_link.append(extract_job_link_indeed(job_elem))
        date.append(extract_date_indeed(job_elem))
        description.append(extract_description_indeed(job_elem))
        i += 1
        print(i)

    results = pd.DataFrame(title, columns=["title"])
    results["company"] = company
    results["date"] = date
    results["description"] = description
    results["application_link"] = application_link

    return(results)


    
# %%

job_title = "'data science' OR 'data scientist'"
location = "Hovedstaden og Bornholm"
Offset = 0

def load_jobnet_jobs_div(job_title, location, Offset=0):
    getVars = {'SearchString' : job_title, 'Region' : location, "WorkHours" : "Fuldtid", "JobAnnouncementType" : "Almindelige Vilkår", "Offset" : Offset, 'SortValue' : 'CreationDate'}
    url = ('https://job.jobnet.dk/CV/FindWork?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup





# %%

# selenium pga angular js
from selenium import webdriver
driver = webdriver.Firefox()

driver.get('https://job.jobnet.dk/CV/FindWork?SearchString=%27Data%2520Science%27%2520OR%2520%27data%2520scientist%27&Region=Hovedstaden%2520og%2520Bornholm&WorkHours=Fuldtid&JobAnnouncementType=Almindelige%2520Vilk%25C3%25A5r&Offset=0&SortValue=CreationDate')

driver.find_element_by_css_selector('[id="declineButton"]').click()
prices = driver.find_element_by_class_name('result-count-label').text
for price in prices:
    print(price.text)
prices.text
driver.close()

soup = BeautifulSoup(driver.page_source, 'lxml')
# %%



def find_number_of_pages_jobnet(job_soup): # TODO
    page_nr = job_soup.find_all("div", class_="result-count-label")
    for pag in page_nr:
        print(pag)



    page_nr = re.findall(r"(\d+) jobs", str(page_nr))[0]
    number_of_pages = math.ceil(int(page_nr) / 20)
    return number_of_pages




# %%







def get_job_view(jobkey, proxies):
    getVars = {'jk' : jobkey, "vjs" : "3"}
    url = ('https://dk.indeed.com/viewjob?' + urllib.parse.urlencode(getVars))
    page = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup



job_soup = load_jobnet_jobs_div(job_title, location)

for overview_page in range(number_of_pages):
    start_page = (overview_page) * 50
    print(start_page)
    job_soup = load_indeed_jobs_div(job_title, location, job_type, start_page)
    job_elems = job_soup.find_all("a", id=re.compile("job_"))
    for job in job_elems:
        job_links.append(re.findall(r"data-jk=\"(.[\w]+)",str(job))[0])

soup
# Set up dockerization
# Set up github actions regualr run
# Set up bash script for running
# Set up data cleaning
# Set up analysis - content?
# Set up overview of jobs
# Set up visualization? - content?
# Set up API? - content?
# %%
