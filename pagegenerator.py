import csv

class Chicken:
	def __init__(self, name = "", year = 0, alive = True, breed = "", description = ""):
		self.name = name
		self.alive = alive
		self.year = year
		self.breed = breed
		self.description = description


currentWorkingFile = "2007.html"
chickens = []
years = ["all"]
navButtonHTML = []

def defineYears():
	yearlist = []
	for chicken in chickens:
		yearlist.append(int(chicken.year))
	for year in range(min(yearlist), max(yearlist)+1):
		years.append(str(year))

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
		
def createIndivPages():
	for chicken in chickens:
		file = open("indiv/" + chicken.name + ".html", "w")
		for line in open("chicken_page_template.html", "r"):
			file.write(line)
			if line == "<!--INSERT-DESCRIPTION-->\n":
				file.write("<h1>" + chicken.name + "</h1>\n")
				file.write("<p>" + chicken.description + "</p>\n")
			elif line == "<!--INSERT-NAV-BUTTONS-->\n":
				makeNavButtonHTML(chicken.year, True)
				for navButton in navButtonHTML:
					file.write(navButton)
		file.close()
		
	
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
			htmlarray.append("<a href=\"indiv/" + chicken.name + ".html\"><div class=\"thumb " + aliveText + " \" style=\"opacity:1;\"><h3>" + chicken.name + "</h3><div><img src=\"images/prof/" + chicken.name + ".jpg\"/></div></div></a>\n\n")

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
readCSVToObj("db3.tsv")
defineYears()
insertHTML()
createIndivPages()