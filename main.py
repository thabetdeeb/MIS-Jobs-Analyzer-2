import sqlite3
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


DB_NAME = "north_is_jobs.db"


IS_KEYWORDS = [
    "מערכות מידע",
    "מנתח מערכות",
    "מיישם מערכות",
    "ERP",
    "CRM",
    "SQL",
    "BI",
    "Data Analyst",
    "Business Analyst",
    "Help Desk",
    "תמיכה טכנית",
    "Priority",
    "SAP",
    "אפיון",
    "דוחות",
    "Power BI",
    "Excel",
    "Database",
]


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        description TEXT,
        requirements TEXT,
        contact_email TEXT,
        contact_phone TEXT,
        source_url TEXT,
        score INTEGER,
        category TEXT,
        source TEXT
    )
    """)

    cursor.execute("DELETE FROM jobs")
    conn.commit()
    conn.close()


def is_north_job(text):
    text = str(text).lower()

    north_words = [
        "חיפה", "קריות", "קרית", "קריית", "עכו", "נהריה",
        "כרמיאל", "צפת", "טבריה", "קריית שמונה", "קצרין",
        "עפולה", "נוף הגליל", "נצרת", "מעלות", "יוקנעם",
        "גליל", "גולן", "צפון", "הצפון"
    ]

    bad_locations = [
        "תל אביב", "רמת גן", "גבעתיים", "פתח תקווה",
        "ראשון לציון", "חולון", "בת ים", "הרצליה",
        "ירושלים", "באר שבע", "אשדוד", "מרכז", "דרום"
    ]

    has_north = any(word in text for word in north_words)
    has_bad = any(word in text for word in bad_locations)

    return has_north and not has_bad


def is_real_job(text):
    text = str(text).lower()

    job_words = [
        "דרוש", "דרושה", "דרושים", "משרה", "עבודה",
        "job", "jobs", "hiring", "career", "הגש מועמדות"
    ]

    is_words = [
        "מערכות מידע", "מנתח מערכות", "מיישם",
        "sql", "bi", "power bi", "erp", "crm",
        "data analyst", "business analyst", "sap",
        "priority", "database", "help desk"
    ]

    bad_words = [
        "חדשות", "כתבה", "ראיון", "ספורט", "פוליטיקה",
        "מלחמה", "תאונה", "רכילות", "פרסום", "ynet",
        "וואלה", "mako", "ישראל היום"
    ]

    has_job_word = any(word in text for word in job_words)
    has_is_word = any(word in text for word in is_words)
    has_bad_word = any(word in text for word in bad_words)

    return has_job_word and has_is_word and not has_bad_word


def calculate_score(text):
    score = 0
    text = str(text).lower()

    for keyword in IS_KEYWORDS:
        if keyword.lower() in text:
            score += 20

    return min(score, 100)


def extract_requirements(text):
    requirements = []

    for keyword in IS_KEYWORDS:
        if keyword.lower() in str(text).lower():
            requirements.append(keyword)

    return ", ".join(requirements)


def classify_job(score):
    if score >= 60:
        return "התאמה גבוהה למערכות מידע"
    elif score >= 30:
        return "התאמה בינונית"
    else:
        return "התאמה נמוכה"


def extract_email(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", str(text))
    return match.group(0) if match else ""


def extract_phone(text):
    match = re.search(r"0\d{1,2}-?\d{7}", str(text))
    return match.group(0) if match else ""


def fetch_jobs_from_drushim():
    search_terms = [
        "מערכות מידע",
        "מיישם מערכות מידע",
        "מנתח מערכות",
        "Data Analyst",
        "SQL",
        "Power BI",
        "ERP",
        "BI",
    ]

    jobs = []

    for term in search_terms:
        url = f"https://www.drushim.co.il/jobs/search/{term.replace(' ', '%20')}/"

        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.find_all(["div", "article", "li"])

            for card in job_cards:
                text = card.get_text(" ", strip=True)

                if not is_real_job(text):
                    continue

                if not is_north_job(text):
                    continue

                jobs.append({
                    "title": text[:80],
                    "company": "לא ידוע",
                    "location": "צפון / לבדוק במודעה",
                    "description": text,
                    "source_url": url,
                    "source": "Drushim"
                })

        except Exception as e:
            print("שגיאה ב-Drushim:", e)

    return jobs


def fetch_jobs_from_jobmaster():
    search_terms = [
        "מערכות מידע",
        "מיישם מערכות מידע",
        "מנתח מערכות",
        "Data Analyst",
        "SQL",
        "Power BI",
        "ERP",
        "BI",
    ]

    jobs = []

    for term in search_terms:
        url = f"https://www.jobmaster.co.il/jobs/?q={term.replace(' ', '+')}"

        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.find_all(["div", "article", "li"])

            for card in job_cards:
                text = card.get_text(" ", strip=True)

                if not is_real_job(text):
                    continue

                if not is_north_job(text):
                    continue

                jobs.append({
                    "title": text[:80],
                    "company": "לא ידוע",
                    "location": "צפון / לבדוק במודעה",
                    "description": text,
                    "source_url": url,
                    "source": "JobMaster"
                })

        except Exception as e:
            print("שגיאה ב-JobMaster:", e)

    return jobs


def save_jobs_to_db(jobs):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    seen_jobs = set()

    for job in jobs:
        title = str(job.get("title", "")).strip()
        company = str(job.get("company", "")).strip()
        location = str(job.get("location", "")).strip()
        description = str(job.get("description", "")).strip()
        source_url = str(job.get("source_url", "")).strip()
        source = str(job.get("source", "")).strip()

        full_text = f"{title} {company} {location} {description}"

        if not is_real_job(full_text):
            continue

        if not is_north_job(full_text):
            continue

        job_key = (title.lower(), company.lower(), location.lower())

        if job_key in seen_jobs:
            continue

        seen_jobs.add(job_key)

        score = calculate_score(full_text)
        requirements = extract_requirements(full_text)
        category = classify_job(score)
        email = extract_email(full_text)
        phone = extract_phone(full_text)

        cursor.execute("""
        INSERT INTO jobs (
            title, company, location, description,
            requirements, contact_email, contact_phone,
            source_url, score, category, source
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title, company, location, description,
            requirements, email, phone,
            source_url, score, category, source
        ))

    conn.commit()
    conn.close()


def analyze_jobs():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()

    if df.empty:
        print("לא נמצאו משרות מתאימות")
        return

    bad_locations = [
        "תל אביב", "רמת גן", "גבעתיים", "פתח תקווה",
        "ראשון לציון", "חולון", "בת ים", "הרצליה",
        "ירושלים", "באר שבע", "אשדוד", "מרכז", "דרום"
    ]

    bad_pattern = "|".join(bad_locations)

    df = df[
        ~df.astype(str).apply(
            lambda row: row.str.contains(bad_pattern, na=False).any(),
            axis=1
        )
    ]

    df["clean_title"] = (
        df["title"]
        .astype(str)
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    df = df.drop_duplicates(subset=["clean_title"], keep="first")
    df = df.drop(columns=["clean_title"])

    df.to_excel("north_is_jobs_analysis.xlsx", index=False)

    print("\nקובץ Excel נוצר בהצלחה")
    print("סה״כ משרות בקובץ:", len(df))
    print(df[["title", "company", "location", "score", "category", "source"]])


def main():
    create_database()

    jobs = []

    drushim_jobs = fetch_jobs_from_drushim()
    print("נמשכו", len(drushim_jobs), "משרות מאתר Drushim")
    jobs.extend(drushim_jobs)

    jobmaster_jobs = fetch_jobs_from_jobmaster()
    print("נמשכו", len(jobmaster_jobs), "משרות מאתר JobMaster")
    jobs.extend(jobmaster_jobs)

    print("סה״כ משרות לפני סינון:", len(jobs))

    save_jobs_to_db(jobs)
    analyze_jobs()


if __name__ == "__main__":
    main()