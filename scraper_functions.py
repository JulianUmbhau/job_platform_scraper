# %%
import requests
import os 
import urllib
from bs4 import BeautifulSoup
import re
import math
import pandas as pd
import selenium
# %%


def load_indeed_jobs_div(job_title, location, job_type, start_page="", radius=25):
    getVars = {'q' : job_title, 'l' : location, "radius" : radius, "jt" : job_type, "fromage" : "any", "limit" : 50, "psf" : "advsrch", "from" : "advancedsearch", 'sort' : 'date', "start" : start_page}
    url = ('https://dk.indeed.com/jobs?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def find_number_of_pages_indeed(job_soup):
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
    number_of_pages = find_number_of_pages_indeed(job_soup)
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
# selenium pga angular js
### TODO ###
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options


def setup_driver_firefox(headless, firefox_binary):
    options = Options()
    options.headless = headless
    driver = webdriver.Firefox(firefox_binary, options=options)
    return(driver)


def set_url_jobnet():
    url = 'https://job.jobnet.dk/CV/FindWork?SearchString=%27Data%2520Science%27%2520OR%2520%27data%2520scientist%27&Region=Hovedstaden%2520og%2520Bornholm&WorkHours=Fuldtid&JobAnnouncementType=Almindelige%2520Vilk%25C3%25A5r&Offset=0&SortValue=CreationDate'
    return(url)


def load_jobnet_jobs_div(job_title, location, Offset=0):
    getVars = {'SearchString' : job_title, 'Region' : location, "WorkHours" : "Fuldtid", "JobAnnouncementType" : "Almindelige Vilkår", "Offset" : Offset, 'SortValue' : 'CreationDate'}
    url = ('https://job.jobnet.dk/CV/FindWork?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def press_cookie_decline_jobnet(driver, delay):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'declineButton')))
        driver.find_element_by_css_selector('[id="declineButton"]').click()
    except TimeoutException:
        print("Loading took too much time!")
    return(driver)


def find_number_of_pages_jobnet(driver, delay):
    time.sleep(delay)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'result-count-label')))
        antal_jobopslag_text = driver.find_element_by_class_name('result-count-label').text
    except TimeoutException:
        print("Loading took too much time!")
    antal_jobopslag = re.findall(r"(\d+) jobopslag", antal_jobopslag_text)
    return(antal_jobopslag)

def get_job_ids_from_page(driver):
    elements = driver.find_elements_by_css_selector("a[class='full-width no-text-overflow ng-isolate-scope']")
    job_ids = []
    for link in elements:
        job_ids.append(link.get_attribute("user-behavior-tracking-id"))
    return(job_ids)


def set_url_jobnet_jobs(job_id):
    url = "https://job.jobnet.dk/CV/FindWork/Details/" + job_id
    return(url)



# henter joboverview-sider
# henter links til jobs

# %%
delay = 1
job_title = '"data science"'
location = "København"
job_type = "fulltime"
proxies = {"http" : "http://50.192.195.69:52018", "http1": "http://62.133.168.72:55443"}
# %%

driver = setup_driver_firefox(False, ".")

url = set_url_jobnet()

driver.get(url)

press_cookie_decline_jobnet(driver, delay)

antal_jobopslag = find_number_of_pages_jobnet(driver, delay)

# get ids  from more pages
job_ids = get_job_ids_from_page(driver)

# loop through pages of jobs and get info
url = set_url_jobnet_jobs(job_ids[0])

driver.get(url)




# %%



driver.find_element_by_class_name("joblist-result-content").text


driver.find_elements_by_class_name("ng-scope")[1].text

driver.find_elements_by_class_name("job-ad-summary")[1].get_attribute("href")

driver.find_elements_by_class_name("job-ad-id ng-binding")


driver.find_elements_by_class_name("full-width no-text-overflow ng-isolate-scope")

driver.find_elements_by_css_selector("[aria-label=Jobannonce med ID: 5434869]")



# %%

driver.close()



# Set up dockerization
# Set up github actions regualr run
# Set up bash script for running
# Set up data cleaning
# Set up analysis - content?
# Set up overview of jobs
# Set up visualization? - content?
# Set up API? - content?
# %%
