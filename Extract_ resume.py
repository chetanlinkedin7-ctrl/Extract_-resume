import re  
import sqlite3 
from pathlib import Path 
from pypdf import PdfReader 
PDF_FILE = Path(__file__).with_name("sample_resume.pdf")
DB_FILE = Path(__file__).with_name("contacts.db")


def extract_pdf_text(PDF_FILE): 
    reader = PdfReader(str(PDF_FILE)) 
    full_text = "" 
    for page in reader.pages:
        full_text+= page.extract_text() + "\n"
        
    return full_text

def extract_email(text): 
    email_pattern = r"\w+\.?\w+@\w+\.\w+"
    email = re.findall(email_pattern,text) 
    return email[0] if email else "Not found"  

def find_phone(text):
    Phone_pattern = r"\+?\d{1,2}\s\d+\s\d+"
    phone =  re.findall(Phone_pattern,text)
    return phone[0] if phone else "Not found"


def find_name(text): 
    lines = [line for line in text.split("\n") if line.strip()] 
    return lines[0] if lines else "Unknown"
    

def store_details(name,email,phone_number): 
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS contacts(name text,email text, phone text )")
    conn.execute("INSERT INTO contacts(name,email,phone) VALUES (?,?,?)",(name,email,phone_number))
    conn.commit()
    row_count = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    conn.close()
    return row_count
    
    
      
    



if  not PDF_FILE.exists(): 
    print(f"{PDF_FILE.name} does not exist")
    raise SystemExit(1)


full_text = extract_pdf_text(PDF_FILE)

email = extract_email(full_text) 
phone_number = find_phone(full_text)
name = find_name(full_text)
print(f"Email:{email}") 
print(f"Phone_number:{phone_number}")
print(f"Name:{name}")

details  = store_details(name,email,phone_number)
print(f"Total rows in the {DB_FILE.name} are {details}")
