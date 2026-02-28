
import requests
import json

def genSummarizedJobOutputJSON(query, country="us"):

    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": query,
        "page":"1",
        "num_pages":"1",
        "country": country,
        "date_posted":"all"
        }

    headers = {
        "x-rapidapi-key": "66f37caf8emsh1ca1a67c88a4173p17d7cejsn6bffb3006b50",
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    # print(response.json())

<<<<<<< HEAD
    with open("FullOutput.json", "w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4)

    with open("FullOutput.json", "r", encoding="utf-8") as file:
=======
    with open("/workspaces/HackUSU_Zaymo/FullOutput.json", "w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4)

    with open("/workspaces/HackUSU_Zaymo/FullOutput.json", "r", encoding="utf-8") as file:
>>>>>>> 533819b13beba601e7fa8e2faf73237d017e8403
        fullJobDict = json.load(file)

    sumJobDict = {}

    for jobIndex in range(len(fullJobDict["data"])):
        # sets up the format for each job in the summarized dictionary
        fullJobDictRef = fullJobDict["data"][jobIndex] # partial dictionary reference, will give the dictionary for each job during that job's interation of the loop
        jobSumTitle = f"{jobIndex + 1}. {fullJobDictRef["job_title"]}"
        sumJobDict[jobSumTitle] = {}

        # create summarized dictionary
        sumJobDict[jobSumTitle]["jobTitle"] = fullJobDictRef["job_title"]
        sumJobDict[jobSumTitle]["employer"] = fullJobDictRef["employer_name"]
        sumJobDict[jobSumTitle]["timeType"] = fullJobDictRef["job_employment_type"]
        sumJobDict[jobSumTitle]["applyOptions"] = fullJobDictRef["apply_options"]
        sumJobDict[jobSumTitle]["description"] = fullJobDictRef["job_description"]
        sumJobDict[jobSumTitle]["location"] = fullJobDictRef["job_location"]

        try:
            sumJobDict[jobSumTitle]["qualificationsList"] = fullJobDictRef["job_highlights"]["Qualifications"]
        except KeyError:
            sumJobDict[jobSumTitle]["qualificationsList"] = None

        try:
            sumJobDict[jobSumTitle]["responsibilitiesList"] = fullJobDictRef["job_highlights"]["Responsibilities"]
        except KeyError:
            sumJobDict[jobSumTitle]["responsibilitiesList"] = None

    with open("ExampleSummarizedOutput.json", "w") as file:
        json.dump(sumJobDict, file, indent=4)

    return sumJobDict
