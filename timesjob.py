import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation='
html_text = requests.get(URL).text
soup = BeautifulSoup(html_text, 'lxml')

# create a list of all job post items
# each item contain the post info related to one job
job_posts = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

# empty containers to store the extracted data in
titles = []
companies = []
skills = []
dates = []
links = []
experiences = []
locations = []

# Extract general info from each of the job_posts
for job in job_posts:
    
    # extracting post date
    date = job.find('span', class_ = 'sim-posted').find_all('span')[-1].text.strip().split()[1]
    
    # only extract info if the date is recent
    # 'few' date means it's old post, and will be ignored
    if date != 'few':
        title = job.find('h2').text.strip()
        company = job.find('h3', class_='joblist-comp-name').text.strip()
        skill = job.find('span', class_='srp-skills').text.strip()
        link = job.find('h2').find('a').get('href')

        # Some info are stored inside a single 'li' tag in the job_posts 
        details = job.find('ul', class_ = 'top-jd-dtl clearfix').find_all('li')

        # Extracting experience from the 'li'
        experience = details[0]
        # Removing unwanted text from the experience
        # if this ran more than one time, the experience would not include the unwanted text
        # if the unwanted text is not found, it'll result in an error
        # using try and except to avoid the error resulting from running mutiple times
        try:
            unwanted = experience.find('i').extract()
        except AttributeError:
            pass
        experience = experience.text.strip()

        # Extracting location from the 'li', then removing unwanted text
        location = details[-1]
        try:
            unwanted = location.find('i').extract()
        except AttributeError:
            pass
        location = location.text.strip()

        # Add the info to the lists
        titles.append(title)
        companies.append(company)
        skills.append(skill)
        dates.append(date)
        links.append(link)
        experiences.append(experience)
        locations.append(location)

# Creating the header and value lists for the info found
columns_names = ['Titles', 'Companies', 'Skills', 'Age', 'Links', 'Experiences', 'Locations']
columns_values = [titles, companies, skills, dates, links, experiences, locations]

# creating the dataframe using the values
# initial result have each row contains 1 type of infor, 1st row all titles, ...
# transposing the df to make each each row have 1 value of each column
df = pd.DataFrame(data=columns_values).T

# rename the df columns
df.columns = columns_names


print(df)