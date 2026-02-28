
import requests
import json

# url = "https://jsearch.p.rapidapi.com/search"

# querystring = {
#     "query":"developer jobs in chicago",
#     "page":"1",
#     "num_pages":"1",
#     "country":"us",
#     "date_posted":"all"
#     }

# headers = {
# 	"x-rapidapi-key": "66f37caf8emsh1ca1a67c88a4173p17d7cejsn6bffb3006b50",
# 	"x-rapidapi-host": "jsearch.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())

# with open("/workspaces/HackUSU_Zaymo/ExampleOutput.json", "w") as file:
#     json.dump(response.json(), file, indent=4)

with open("/workspaces/HackUSU_Zaymo/ExampleOutput.json", "r") as file:
    fullJobDict = json.load(file)

def validateDict(sumDict, fullJobDict):
    try:
        sumDict = fullJobDict
    except KeyError:
        sumDict = None
    
    return sumDict


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

with open("/workspaces/HackUSU_Zaymo/ExampleSummarizedOutput.json", "w") as file:
    json.dump(sumJobDict, file, indent=4)


