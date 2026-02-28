from google import genai
import os
from CallJSearch import genSummarizedJobOutputJSON as jobOutput
import json
# Loads the .env file into the environment variables
def _load_dotenv_if_present(dotenv_path: str = ".env") -> bool:
    try:
        if not os.path.exists(dotenv_path):
            return False
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                os.environ.setdefault(k, v)
        return True
    except Exception:
        return False


dotenv_loaded = _load_dotenv_if_present(".env")
gemini_api_key = os.getenv("GEMINI_API_KEY")
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
if not gemini_api_key:
    raise ValueError("Missing GEMINI_API_KEY in environment (did you load .env?)")
client = genai.Client(api_key=gemini_api_key)

resume_path = "public/AI Ready Resume.docx"
# Checks if the python-docx library is installed
try:
    import docx  # type: ignore[import-not-found]
except ImportError as e:
    print("'python-docx' library required to read resume, install it in the virtual environment with 'pip install python-docx'")

# Checks if the resume file exists
if not os.path.exists(resume_path):
    raise FileNotFoundError(f"Resume file not found: {resume_path}")
doc = docx.Document(resume_path)
job = json.load(open("oneJob.json", "r", encoding="utf-8"))
# Generates the Gemini response for the jobs
# Writes the response to a file
def generate_gemini_response(doc, job): #job_dict
    resume_text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    # for job in job_dict.keys():
    base_prompt = "Role: Career Coach;" # Check indentation when swapping between full Jsearch API call and one job for testing Gemini response
    prompt = (
        " Step 2: Identify gaps in the resume relative to this job title and description: "
        # + job_dict[job]["jobTitle"] + "\n" + job_dict[job]["description"]
        + job["jobTitle"] + " at " + job["employer"] + "\n" + job["description"]
        + """\nStep 3: Provide a list of 3 key skills to develop, 
            and a list of 3 concise resume changes to make (50 words or less).
            Step 4: Format output as follows:
            <job title>: company name and job title
            <resume gaps>: list of identified gaps
            <key skills to develop>: list of 3 key skills to develop
            <resume changes to make>: list of 3 concise resume changes to make (50 words or less)
            All labeled clearly with headers and use bulleted lists. Optimize for concise and readable output."""
    )

    full_prompt =base_prompt + "Step 1:Read this resume content:\n\n" + resume_text + "\n\n" + prompt
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[full_prompt],
        config={"http_options": {"timeout": 60000}},
    )
    with open("gemini_response_test.txt", "w", encoding="utf-8") as file:
        file.write(response.text)
    return response.text

# job_dict = jobOutput(input("Enter a job title and location (e.g. 'Data Analyst (Intern) in Washington, DC'): ")) <- Full Jsearch API call
# job_dict = json.load(open("ExampleSummarizedOutput.json", "w", encoding="utf-8")) <- Example output from Jsearch API call (several jobs   )
# generate_gemini_response(doc, job_dict) <- Full Jsearch API call and Gemini response
generate_gemini_response(doc, job) # One job for testing Gemini response
print("Gemini response generated and saved to gemini_response.txt")
