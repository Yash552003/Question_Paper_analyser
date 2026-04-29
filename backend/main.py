import io
import os
import concurrent.futures
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
from google import genai
from google.genai import errors
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# --- SECURITY & CORS ---
# Essential for Chrome and Mobile communication
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
)

# --- CONFIGURATION ---
# Use the modern Gemini 2.0 Flash for speed and higher token limits
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set!")

client = genai.Client(api_key=GOOGLE_API_KEY)
GEMINI_MODEL = "gemini-2.0-flash"

def extract_text_from_pdf(file_content):
    """Worker function to extract text from PDF bytes."""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        # Extracting first 4 pages of each paper to keep token count low/fast
        text = ""
        for page in reader.pages[:4]:
            text += page.extract_text()
        return text
    except Exception:
        return ""

@app.get("/")
def home():
    return {"status": "Bramha Universal Server Online", "version": "2.0-Flash"}

@app.post("/analyze")
async def analyze_papers(files: List[UploadFile] = File(...)):
    try:
        # 1. Read all files into memory asynchronously
        file_contents = [await f.read() for f in files]
        
        # 2. Parallel Text Extraction (Fastest method for multi-file)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            extracted_texts = list(executor.map(extract_text_from_pdf, file_contents))
        
        combined_context = ""
        for i, text in enumerate(extracted_texts):
            combined_context += f"\n--- PAPER {i+1} ---\n{text}\n"

        # 3. The Universal Brain Prompt
        # This works for any subject (IT, Mech, Civil, etc.)
        prompt = f"""
        You are a Mumbai University Professor and Exam Expert. 
        Analyze these {len(files)} question papers:
        
        {combined_context[:12000]} 

        TASK:
        1. Identify the Subject and the Mumbai University Scheme (e.g., Rev-2019 'C' Scheme).
        2. Frequency Analysis: Identify questions or topics that appear in multiple papers.
        3. Practical/Numerical Patterns: Which calculation-based questions are guaranteed?
        4. Study Strategy: Provide a prioritized 'Master IMP' list for a student to pass in 24 hours.
        """

        # 4. Generate Content with latest SDK
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return {
            "subject": "Automatic Detection",
            "analysis": response.text
        }

    except errors.ClientError as e:
        # Graceful handling for Quota/Rate Limit issues
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return {"analysis": "### ⚠️ Bramha is thinking too hard!\nGoogle's free-tier limit reached. Please wait 60 seconds and try again."}
        return {"analysis": f"Error: {str(e)}"}
    except Exception as e:
        return {"analysis": f"An unexpected error occurred: {str(e)}"}