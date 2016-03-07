import csv
import os

class Chicken:
	def __init__(self, name = "", year = 0, alive = True, breed = "", description = ""):
		self.name = name
		self.alive = alive
		self.year = year
		self.breed = breed
		self.description = description


# currentWorkingFile = "2007.html"
chickens = []
years = ["all"]
navButtonHTML = []


# adds the years listed in the chicken objects
def defineYears():
	yearlist = []
	for chicken in chickens:
		yearlist.append(int(chicken.year))
	for year in range(min(yearlist), max(yearlist)+1):
		years.append(str(year))

# creates a page for each year and adds the chicken buttons to it
# ex. "2012.html"
def insertHTML():
	for year in years:
		chickenButtonHTMLToInsert = convertObjToHTML(year)
		file = open(year + ".html", "w")
		for line in open("year_page_template.html", "r"):
			file.write(line)
			if line == "<!--INSERT-PAGE-TITLE-->\n":
				if year == "all":
					file.write("<h1>The chickens hatched in all years</h1>")
					file.write("<p>In order of year hatched.</p>")
				elif year != "index":
					file.write("<h1>The chickens hatched in " + year + "</h1>")
			elif line == "<!--INSERT-NAV-BUTTONS-->\n":
				makeNavButtonHTML(year)
				for navButton in navButtonHTML:
					file.write(navButton)
			elif line == "<!--INSERT-CHICKENS-->\n" :
				for chickenButtonHTML in chickenButtonHTMLToInsert:
					file.write(chickenButtonHTML)
		file.close()

# creates a page for each chicken
# ex. "Gordo.html"		
def createIndivPages():
	for chicken in chickens:
		if not os.path.exists("chicken/" + chicken.name.lower()):
			os.makedirs("chicken/" + chicken.name.lower())
		file = open("chicken/" + chicken.name.lower() + "/" + chicken.name.lower() + ".html", "w")
		for line in open("chicken_page_template.html", "r"):
			file.write(line)
			if line == "<!--INSERT-DESCRIPTION-->\n":
				file.write("<h1>" + chicken.name + "</h1>\n")
				file.write("<p>" + chicken.description + "</p>\n")
				for detailImageHTML in makeDetailImageHTML(chicken):
					file.write(detailImageHTML)
			elif line == "<!--INSERT-NAV-BUTTONS-->\n":
				makeNavButtonHTML(chicken.year, True)
				for navButton in navButtonHTML:
					file.write(navButton)
		file.close()

# generates an array of html for the images to be put in the description of the individual chicken pages
def makeDetailImageHTML(chicken):
	detailImageHTMLArray = []
	return detailImageHTMLArray
		
# reads a tsv file and creates Chicken objects in the array "chickens"	
def readCSVToObj(currentCSV = ""):
	with open(currentCSV, "r") as csvfile:
		csvReader = csv.reader(csvfile, delimiter="\t")
		currentRow = 0
		for row in csvReader:
			alive = True
			if currentRow>0:
				if row[2] == "d":
					alive = False
				chickens.append(Chicken(row[0], row[1], alive, row[3], row[4]))
			currentRow += 1

# makes the html for the chicken buttons
def convertObjToHTML(year):
	htmlarray = []
	for chicken in chickens:
		aliveText = ""
		if not chicken.alive:
			aliveText = "d"
		if chicken.year == year or year == "all":
			htmlarray.append("<a href=\"chicken/" + chicken.name.lower() + "\"><div class=\"thumb " + aliveText + " \" style=\"opacity:1;\"><h3>" + chicken.name + "</h3><div><img src=\"chicken/" + chicken.name.lower() + "/" + chicken.name + ".jpg\"/></div></div></a>\n")

	return htmlarray
			
# makes navigation bar
# takes in current year as a number, 0 is all years
def makeNavButtonHTML(currentYear, indiv = False):
	navButtonHTML.clear()
	current = ""
	upDir = ""
	if indiv:
		upDir = "../"
	for year in years:
		current = ""
		if year ==  "all":
			if currentYear == "all":
				current = "current"
			navButtonHTML.append("<a href=\"" + upDir + "all.html\"><li class=\"navbutt " + current + "\">ALL YEARS</li></a>\n")
		else:
			if currentYear == year:
				current = "current"
			navButtonHTML.append("<a href=\"" + upDir + year + ".html\"><li class=\"navbutt " + current + "\">" + year + "</li></a>\n")

#readCSV("db.csv")
readCSVToObj("db.tsv")
defineYears()
insertHTML()
createIndivPages()
