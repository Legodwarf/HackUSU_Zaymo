## Automatic Job Searcher and Resume Tailor
This application allows you to search all major job boards for a job title in a location of your choice. It also feeds a copy of your resume to Gemini (Can sub for your AI of choice if you modify the code) which provides resume tailoring for each job returned.

** Data Security/Privacy Note: Do not include Personal Identifiable Information in your resume (and probably best practice to acvoid this with AI generally) as Gemini will read it and we don't know what exactly it does with that **

Requirements to run:
Supply in a .env file
- Your own Gemini API key (Google AI Studio)
- Your own Jsearch API key (Found on RapidAPI)

- upload resume to ai, have it identify strengths/jobs you'd be interested in
- call api and get job data for jobs
- ask ai how resume could be updated for each job
- Output results in chatbot form


FOR SATURDAY
- make a UI
- publish to docker
- publich to selecteez.com