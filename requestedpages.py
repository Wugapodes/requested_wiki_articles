#!/usr/bin/python
import pywikibot
from pywikibot import pagegenerators

def main(site, Wikiproject, Category, Threshold):
	cat = pywikibot.Category(site, Category)
	gen = pagegenerators.CategorizedPageGenerator(cat)
	redlinks  = {}
	for page in gen:
		article = page.toggleTalkPage()
		linkgen = article.linkedPages()
		for link in linkgen:
			if link.exists() != True:
				if link.title() in redlinks:
					redlinks[link.title()] = redlinks[link.title()] + 1
				else:
					redlinks[link.title()] = 1
	# Writing output to page
	listpage = pywikibot.Page(site, 'User:ProjectRequestedPagesBot/Most Requested '+ Wikiproject +' pages')
	entries = len(redlinks)
	if entries < 1:
		listpage.put('No redlinks found', summary='No redlinks found', minorEdit=False)
	else:
		text = createPage(redlinks, entries, Threshold)
		listpage.put(text, summary='Adding the '+entries+' most requested articles in the '+Wikiproject+' scope', minorEdit=False)
	print text

def createPage(dictionary, length, thresh):
	text = ''
	entries = sortDict(dictionary)
	for i in range(len(entries)):
		if entries[i][1] > thresh: #only includes entry if number of links is greater than the project specified threshold
			text = text + '# [[' + entries[i][0] + ']] &mdash; ' + str(entries[i][1]) + '\n'
	return text
	
def sortDict(dictionary):
	entries = []
	for key in dictionary:
		entries.append([key,dictionary[key]])
	sortedEntries = sort(entries)
	return sortedEntries
	
def sort(array): #quicksort the entries
	ls = []
	eq = []
	gr = []
	if len(array) > 1:
		pivot = array[0][1]
		for x in array:
			if x[1] < pivot:
				ls.append(x)
			elif x[1] == pivot:
				eq.append(x)
			elif x[1] > pivot:
				gr.append(x)
		return sort(ls)+eq+sort(gr)
	else:
		return array
		
def getProjects(site):
	projects = list()
	master = pywikibot.Page(site, 'User:ProjectRequestedPagesBot/Master')
	mastertext = master.get()
	for line in mastertext.splitlines():
		line = line.split(',')
		projects.append(line)
	return projects
	
def isint(item):
	try:
		int(item)
		return True
	except:
		return False 

site = pywikibot.Site()
projects = getProjects(site)

for item in projects:
	Wikiproject = item[0] #first item on a line is the name of the wikiproject
	Category    = item[1] #second item on a line is the category name
	if isint(item[2]) and int(item[2]) > 0: #checks to make sure threshold is an actual integer and that it is not negative
		Threshold = int(item[2]) 
	else:
		Threshold = 0 #defaults to listing every entry
	main(site, Wikiproject, Category, Threshold) #goes to main execution
sys.exit()
