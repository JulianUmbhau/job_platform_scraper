# %%
from scraper_functions import scrape_indeed
import pandas as pd

# %%

job_title = '"data science"'
location = "København"
job_type = "fulltime"
proxies = {"http" : "http://50.192.195.69:52018", "http1": "http://62.133.168.72:55443"}

results = scrape_indeed(job_title, location, job_type, proxies)

results.to_csv("./joblist.csv")

# %%
