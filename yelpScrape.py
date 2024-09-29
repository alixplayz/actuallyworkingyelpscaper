import re
import requests
from bs4 import BeautifulSoup
import csv

theUrl = input("Paste the yelp url (go to yelp, search for the niche you want and the location and just copy that url): ")
numberOfPages = int(input("Enter number of pages the yelp search has (scroll to the bottom of the yelp page and keep going to the last page until there is no more, then write the number one): "))
input("Ok awesome enjoy. \n It will print all the businesses out in the terminal. \n You can press control + c if you want to end it early. \n The results will end up in 'results.csv'. \n After that you will have to clean up the names a bit \n Then just import the csv into google sheets (directly to highlevel probably works too) and boom, beautiful leads. \n But since it only gets some of the owners names, I'd recommend you try and google the rest of them manually and find there names before importing it to gohighlevel and cold calling \n PRESS ENTER TO START")
EveryBusiness = []

# ignore these 3 variables lol im too scared to remove them too incase it breaks something
Name = []
Company = []
Phone = []

with open('results.csv', 'w', newline='') as file:

    writer = csv.writer(file)
    field = ["Name", "Company", "Phone", "Yelp"]
    writer.writerow(field)

    loopTimes = 0
    while loopTimes < numberOfPages*10-10:

        Yelp = []

        html = requests.get(theUrl + "&start=" + str(loopTimes)).text
        soup = BeautifulSoup(html)

        # Yelp
        yelpTemp = []
        for link in soup.find_all('a'):
            if str(link.get('href')).__contains__("/biz/"):
                yelpTemp.append(str(link.get('href')).split("?")[0])
        # remove dupes
        [Yelp.append(x) for x in yelpTemp if x not in Yelp]

        # go to Yelp urls to start getting rest of information
        for bizurl in Yelp:
            EachBusiness = []

            bizurlHtml = requests.get("https://www.yelp.ca" + str(bizurl))
            bizurlSoup = BeautifulSoup(bizurlHtml.text)

            try:
                try:
                    # Name
                    tempName = []
                    rawDawg = bizurlSoup.find_all("p", class_="y-css-w3ea6v")
                    for z in rawDawg:
                        tempName.append(str(z).split(">")[1].split("<")[0])

                    nameString = ""
                    for h in tempName:
                        if str(h).count(" ") == 0 or str(h).count(" ") == 1 or str(h).count(" ") == 2:
                            if str(h) != "Thu" and str(h) != "Wed" and str(h) != "Mon" and str(h) != "Sat" and str(h) != "Sun" and str(h) != "Fri" and str(h) != "Tue" and "Serving" not in str(h) and "%" not in str(h) and "days" not in str(h) and "hours" not in str(h):
                                Name.append(h)
                                if nameString == "":
                                    nameString = nameString + h
                                else:
                                    nameString = nameString + " " + h
                    EachBusiness.append(nameString)
                    

                    # Company
                    if len(EachBusiness) == 0:
                        EachBusiness.append("")
                    Company.append(str(bizurlSoup.find_all("h1", class_="y-css-olzveb")).split(">")[1].split("<")[0])
                    EachBusiness.append(str(bizurlSoup.find_all("h1", class_="y-css-olzveb")).split(">")[1].split("<")[0])

                    # Phone
                    raw = bizurlSoup.find_all("p", class_="y-css-1o34y7f")
                    for x in raw:
                        a = str(x).split(">")[1].split("<")[0]
                        if a.count("(") == 1 and a.count(")") == 1 and a.count("-") == 1 and a.count(" ") == 1:
                            Phone.append(a)
                            EachBusiness.append(a)

                    # Yelp
                    EachBusiness.append(bizurl)
                    print(EachBusiness)

                    # Add to EveryBusiness
                    if EachBusiness not in EveryBusiness:
                        writer.writerow(EachBusiness)
                        EveryBusiness.append(EachBusiness)
                except KeyboardInterrupt:
                    print("end")
                    continue

            except Exception as e:
                continue

        loopTimes = loopTimes + 10
        print("next page")
    
    print(EveryBusiness)
