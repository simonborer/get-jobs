from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re

def getHTML(url):
	req = Request(url, headers={'User-Agent' : "Magic Browser"}) 
	con = urlopen( req )
	return con.read();

def printJobs(title = '?', link = '?'):
	print(re.sub(' +', ' ','\n## ' + title.replace('\n', ' ').replace('\r', '') + '\n🔗 ' + link + '\n'))
	return;

def jobToParse( label, link ):
   j = dict();
   j['label'] = '\n\n# ' + label
   j['link'] = link
   j['content'] = BeautifulSoup(getHTML(link), 'html.parser')
   return j;

nfb = jobToParse('NFB', 'https://jobs.nfb.ca/jobs')
tpl = jobToParse('TPL', 'https://www.torontopubliclibrary.ca/about-the-library/library-jobs/')
moca = jobToParse('MOCA', 'https://moca.ca/careers/')
# cbc = jobToParse('CBC', 'https://cbc.taleo.net/careersection/2/jobsearch.ftl?lang=en&tzname=America%2FToronto')
ago = jobToParse('AGO', 'https://jobs.jobvite.com/ago/jobs/viewall')
city = jobToParse('City', 'https://jobs.toronto.ca/jobsatcity/search/?createNewAlert=false&q=web')

NFBjobs = nfb['content'].find_all("li", class_="job-item")
TPLjobs = tpl['content'].find(id="Content").find("ul", class_="no-bullet").find_all("li")
MOCAjobs = moca['content'].find(attrs={"data-elementor-type": "single-page"}).find_all("a")
# CBCjobs = cbc['content'].find(id="jobList").find_all("li")
AGOjobs = ago['content'].find_all("h3", class_="h2")
Cityjobs = city['content'].find(id="job-tile-list").find_all("tr")

print(nfb['label'])
for job in NFBjobs:
	joblocation = job.find(class_="job-location")
	if 'Toronto' in joblocation.text.strip():
		jobtitle = job.find(class_="job-title")
		joblink = job.a.get('href')
		printJobs(jobtitle.text.strip(), joblink)

print(tpl['label'])
for job in TPLjobs:
	jobtitle = job.h3
	joblink = jobtitle.a.get('href')
	printJobs(jobtitle.text.strip(), joblink)

# MOCA's website is a misery to parse, built with a visual page builder
print(moca['label'])
for job in MOCAjobs:
	joblink = job.get('href')
	printJobs(link = joblink)

print('\n## CBC')
print('Unlike MOCA, CBC has the decency to be completely inaccessible without importing webdriver and waiting for the page to load. Holy jQuery UI.')
print('Best to just go to \n🔗 https://cbc.taleo.net/careersection/2/jobsearch.ftl?lang=en&tzname=America%2FToronto')

catsToIgnore = ['Beverage', 'Plant Operations', 'Conservation', 'Finance']

print(ago['label'])
for job in AGOjobs:
	if any(cat in job.text.strip() for cat in catsToIgnore):
		print('\n(Ignored ' + job.text.strip() + ')')
	else:
		cat = job.find_next("ul")
		catJobs = cat.find_all("li")
		for j in catJobs:
			printJobs(j.text.strip(), 'https://jobs.jobvite.com/' + j.a.get('href'))

# This took a little golfing because they have each link duplicated a bunch of times
print(city['label'])
for job in Cityjobs:
	j = job.find("a")
	printJobs(j.text.strip(), j.get('href'))

print('\n## UHN')
print('Best to just go to \n🔗 https://www.recruitingsite.com/csbsites/uhncareers/careers.asp')


print('\n\n')