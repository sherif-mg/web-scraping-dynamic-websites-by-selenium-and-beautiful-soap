import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#options=FirefoxOptions()
#options.headless=True
driver=Firefox()

#request =requests.get("https://wuzzuf.net/search/jobs/?q=python&a=navbg")

#src=request.content
#driver.find_element(By.CSS_SELECTOR,".css-if9uys .css-e5a93e .css-1q4vxyr .css-zye1os ezfki8j0")

job_titles_txt = []
links = []
companies_name_txt = []
companies_location_txt = []
time_txt = []
skills_txt = []
salary = []

#main page with search box
mainPage="https://wuzzuf.net/jobs/egypt"

#search word
search="php"

driver.get(mainPage)

searchBox=driver.find_element(By.CSS_SELECTOR,".search-bar-input")
searchButton=driver.find_element(By.CSS_SELECTOR,".search-btn")
searchBox.send_keys(search)
searchButton.click()

#get target url
get_url = driver.current_url+"&start=%s"

index = 0

#while loop to get all pages of the job
while True:
    driver.get(get_url%index)

    soup=BeautifulSoup(driver.page_source,"lxml")

    job_titles=soup.find_all("a",{"class":"css-o171kl","rel":"noreferrer"})
    companies_name=soup.find_all("a",{"class":"css-17s97q8","rel":"noreferrer"})
    companies_location=soup.find_all("span",{"class":"css-5wys0k"})
    time=[ div.find_all("span",{"class":"css-1ve4b75 eoyjyou0"}) for div in soup.find_all("div",{"class":"css-1lh32fc"})]
    skills=soup.find_all("div",{"class":"css-y4udm8"})

    for i in range(len(job_titles)):
           job_titles_txt.append(job_titles[i].text)
           links.append("https://wuzzuf.net"+job_titles[i].attrs['href'])
           companies_name_txt.append(companies_name[i].text)
           companies_location_txt.append(companies_location[i].text)
           time_txt.append([span.text for span in time[i]])
           skills_txt.append(skills[i].select('div:nth-of-type(2)')[0].text )

    if len(job_titles) == 0:
        break
    else:
        index+=1


#for loop to go to page of each job advertisement
#to get info about salary
for idx,link in enumerate(links):
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, "lxml")
    salary.append(soup.findAll("span", {"class": "css-4xky9y"})[3].text)






file_list=[job_titles_txt,companies_name_txt,companies_location_txt,salary,time_txt,skills_txt,links]
exported=zip_longest(*file_list)

#save data in csv file
with open(search+"_jobs.csv","w", newline='') as myfile:
    wr=csv.writer(myfile)
    wr.writerow(["job title","company name","location","salary","type of employment","skills","links"])
    wr.writerows(exported)

driver.quit()
