# %%
import requests
import os 
import urllib
from bs4 import BeautifulSoup

# %%
def load_indeed_jobs_div(job_title, location, job_type):
    getVars = {'q' : job_title, 'l' : location, "jt" : job_type, 'sort' : 'date'}
    url = ('https://dk.indeed.com/jobs?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

# %%
job_soup = load_indeed_jobs_div("data science", "København", "fulltime")


# %%

job_elems = job_soup.find_all("a", id=re.compile("job_"))


# %%
job_links = []
for job in job_elems:
   test = str(job)
   job_links.append(re.findall(r"data-jk=\"(.[\w]+)",test)[0])

# %%

def get_job_view(jobkey):
    getVars = {'jk' : jobkey, "vjs" : "3"}
    url = ('https://dk.indeed.com/viewjob?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

# %%
for job_link in job_links:
    job_elem = get_job_view(job_link)
    job_title = extract_job_title_indeed(job_elem)

# %%

def extract_job_title_indeed(job_elem):
    title_elem = soup.find("div", class_="jobsearch-JobInfoHeader-title-container")
    title = title_elem.text.strip()
    return title

def extract_company_indeed(job_elem):
    company_elem = job_elem.find('span', class_='companyName')
    company = company_elem.text.strip()
    return company

def extract_jobcard_indeed(job_elem):
    link = job_elem.find('a')['href']
    link = 'dk.Indeedcom/' + link
    return link

def extract_date_indeed(job_elem):
    date_elem = job_elem.find('span', class_='date')
    date = date_elem.text.strip()
    return date






#%%


# %%
import re
job_elems = job_soup.find_all('a', href=True)


# %%
job = job_elems[0]
# %%
for job in job_elems:
    print(extract_job_title_indeed(job))
    print(extract_company_indeed(job))
    print(extract_link_indeed(job))
    print(extract_date_indeed(job))


    
# %%
