import sys; siteNum = sys.argv[1:]
import requests, re

def createInstantaneousURL(inputNum):
    url = "https://waterservices.usgs.gov/nwis/iv/?format=json&indent=on&sites=" + (inputNum) + "&siteStatus=all"
    return url

def parseInstantData(response):
    responseJSON = response.json()
    data = responseJSON["value"]["timeSeries"]
    if data == []:
        return -1
    information = []
    for valueSet in data:

        #source info
        siteName = valueSet["sourceInfo"]["siteName"]
        siteCode = valueSet["sourceInfo"]["siteCode"][0]["value"]
        latitude = valueSet["sourceInfo"]["geoLocation"]["geogLocation"]["latitude"]
        longitude = valueSet["sourceInfo"]["geoLocation"]["geogLocation"]["longitude"]

        #variable info
        variableName = valueSet["variable"]["variableName"]
        variableDescription = valueSet["variable"]["variableDescription"]
        unit = valueSet["variable"]["unit"]["unitCode"]
        value = valueSet["values"][0]["value"][0]["value"]
        time = valueSet["values"][0]["value"][0]["dateTime"]
        info = [siteName,siteCode,latitude,longitude,variableName,variableDescription,unit,value,time]
        information.append(info)
    return information


def display(information):
    # print("info - [siteName,siteCode,latitude,longitude,variableName,variableDescription,unit,value,time]")
    # for info in information:
    #     print(info)
    print("Site Name: " + str(information[0][0]))
    print("Site Code: " + str(information[0][1]))
    print("Latitude: " + str(information[0][2]))
    print("Longitude Name: " + str(information[0][3]))

    for info in information:
        varName = str(info[4])
        varName = re.sub(r",.*","",varName)
        print(varName + ": " + str(info[5]))
        print("\t" + str(info[7]) + " " + str(info[6]) + " at " + str(info[8]))


def main():
    inputNum = siteNum[0]
    instantURL = createInstantaneousURL(inputNum)
    instantResponse = requests.get(instantURL)
    information = parseInstantData(instantResponse)
    if information == -1:
        print("No Site Data Found")
    else:
        display(information)

if __name__ == '__main__':
    main()