from google import genai
import os
from CallJSearch import genSummarizedJobOutputJSON as jobOutput

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
job_description = os.getenv("JOB_DESCRIPTION")
gemini_api_key = os.getenv("GEMINI_API_KEY")
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
if not gemini_api_key:
    raise ValueError("Missing GEMINI_API_KEY in environment (did you load .env?)")
client = genai.Client(api_key=gemini_api_key)

resume_path = "public/AI Ready Resume.docx"
try:
    import docx  # type: ignore[import-not-found]
except ImportError as e:
    raise ImportError(
        "The 'python-docx' package is required to read the resume. "
        "Install it with: /Users/stephenparker/Documents/HackUSU_Zaymo/.venv/bin/python -m pip install python-docx"
    ) from e

if not os.path.exists(resume_path):
    raise FileNotFoundError(f"Resume file not found: {resume_path}")

doc = docx.Document(resume_path)
resume_text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
job_dict = jobOutput("Data Analyst (Intern) in Washington, DC")
for job in job_dict.keys():
    base_prompt = "Role: Career Coach; Task: Identify gaps in the resume"
    prompt = (
        base_prompt
        + " relative to this job description: "
        + job_dict[job]["description"]
        + " and provide a list of 3-5 potential resume improvements."
    )

    full_prompt = "Here is the resume content:\n\n" + resume_text + "\n\n" + prompt
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[full_prompt],
        config={"http_options": {"timeout": 60000}},
    )
    print(response.text)
    with open("gemini_response.txt", "w") as file:
        file.write(response.text)