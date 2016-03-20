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
years = ["all", "unknown"]
navButtonHTML = []


# adds the years listed in the chicken objects
def defineYears():
	yearlist = []
	for chicken in chickens:
		if chicken.year != "unknown":
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
				elif year == "unknown":
					file.write("<h1>The chickens with an unknown hatch date.</h1>")
					file.write("<p>If you know the hatch date of one of these chickens, record your knowledge <a href=\"https://docs.google.com/spreadsheets/d/1ePVBvv94f_LUNXYxrVJlI0ZJmNAwarL00pfcorK66nU/edit#gid=0\" >here.</a></p>")
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
# ex. "chicken/gordo/index.html"
def createIndivPages():
	for chicken in chickens:
		file = open("chicken/" + chicken.name.lower() + "/" + chicken.name.lower() + ".html", "w")
		for line in open("chicken_page_template.html", "r"):
			file.write(line)
			if line == "<!--INSERT-DESCRIPTION-->\n":
				file.write("<h1>" + chicken.name + "</h1>\n")
				file.write("<h3>Breed: " + chicken.breed + "</h3>\n")
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
	for file in os.listdir("chicken/" + chicken.name.lower()):
		if (file[-4:] == ".jpg" or file[-4:] == ".JPG") and file[:6] != "small_" and file[:4] != "med_":
			detailImageHTMLArray.append("<a href=\"" + file + "\"><img src=\"small_" + file + "\" srcset=\"small_" + file + " 1x, med_" + file + " 2x, " + file + " 4x\" alt=\"" + file + "\"class=\"descriptionImage\" /></a>\n")
			# detailImageHTMLArray.append("<a href=\"" + file + "\"><img src=\"small_" + file + "\" srcset=\"small_" + file + " 320w, ../../images/error.png 640w, " + file + " 2048w\" alt=\"" + file + "\" class=\"descriptionImage\" /></a>\n")
	return detailImageHTMLArray

# reads a tsv file and creates Chicken objects in the array "chickens"
def convertCSVToObj(currentCSV = ""):
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
	makeChickenDirs()

# makes the directories for the chickens
def makeChickenDirs():
	for chicken in chickens:
		if not os.path.exists("chicken/" + chicken.name.lower()):
			os.makedirs("chicken/" + chicken.name.lower())

# makes the html for the chicken buttons
def convertObjToHTML(year):
	htmlarray = []
	for chicken in chickens:
		aliveText = ""
		if not chicken.alive:
			aliveText = "d"
		thumbImageName = "../../images/error.png\" class=\"errorImg\" style=\"width:50px; padding:1em;"
		imageExists = False;
		for file in os.listdir("chicken/" + chicken.name.lower()):
			if (file[-4:] == ".jpg" or file[-4:] == ".JPG") and file[:6] != "small_" and file[:4] != "med_":
				thumbImageName = file
				imageExists = True;
		if chicken.year == year or year == "all":
			if imageExists:
				htmlarray.append("<a href=\"chicken/" + chicken.name.lower() + "/" + chicken.name.lower() + ".html\"><div class=\"thumb " + aliveText + " \" style=\"opacity:1;\"><h3>" + chicken.name + "</h3><div><img src=\"chicken/" + chicken.name.lower() + "/small_" + thumbImageName + "\" srcset=\"chicken/" + chicken.name.lower() + "/med_" + thumbImageName + " 2x, chicken/" + chicken.name.lower() + "/" + thumbImageName + " 4x\" /></div></div></a>\n")
			else:
				htmlarray.append("<a href=\"chicken/" + chicken.name.lower() + "/" + chicken.name.lower() + ".html\"><div class=\"thumb " + aliveText + " \" style=\"opacity:1;\"><h3>" + chicken.name + "</h3><div><img src=\"chicken/" + chicken.name.lower() + "/" + thumbImageName + "\"/></div></div></a>\n")

	return htmlarray

# makes navigation bar
# takes in current year as a number, 0 is all years
def makeNavButtonHTML(currentYear, indiv = False):
	navButtonHTML.clear()
	current = ""
	upDir = ""
	if indiv:
		upDir = "../../"
	for year in years:
		current = ""
		if year ==  "all":
			if currentYear == "all":
				current = "current"
			navButtonHTML.append("<a href=\"" + upDir + "all.html\"><div class=\"navbutt " + current + "\">ALL YEARS</div></a>\n")
		else:
			if currentYear == year:
				current = "current"
			navButtonHTML.append("<a href=\"" + upDir + year + ".html\"><div class=\"navbutt " + current + "\">" + year + "</div></a>\n")

#readCSV("db.csv")
convertCSVToObj("db.tsv")
defineYears()
insertHTML()
createIndivPages()
input("Press Enter to continue...")
