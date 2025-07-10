from typing import List, Dict, Any
import requests
import xml.etree.ElementTree as ET

NON_ACADEMIC_KEYWORDS = [
    "pharma", "biotech", "inc", "ltd", "company", "corp", "gmbh", "s.a.", "llc", "plc", "co.", "industries"
]
ACADEMIC_KEYWORDS = [
    "university", "institute", "hospital", "college", "school", "center", "centre", "academy", "faculty", "department", "research foundation", "clinic"
]

def fetch_pubmed_ids(query: str, retmax: int = 10) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()["esearchresult"]["idlist"]
    except Exception as e:
        raise RuntimeError(f"Failed to fetch PubMed IDs: {e}")

def fetch_paper_details(pmid: str) -> Dict[str, Any]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
    except Exception as e:
        return {
            "PubmedID": pmid,
            "Title": "Error fetching details",
            "Publication Date": "",
            "Non-academic Author(s)": "",
            "Company Affiliation(s)": "",
            "Corresponding Author Email": f"Error: {e}"
        }

    title = root.findtext(".//ArticleTitle") or ""
    pub_date = root.findtext(".//PubDate/Year") or "Unknown"

    authors: List[str] = []
    companies: List[str] = []
    email: str = ""

    for author in root.findall(".//Author"):
        affiliation = author.findtext(".//AffiliationInfo/Affiliation") or ""
        fore_name = author.findtext("ForeName") or ""
        last_name = author.findtext("LastName") or ""
        name = f"{fore_name} {last_name}".strip()
        affil_lower = affiliation.lower()
        # Heuristic: must have non-academic keyword and not academic keyword
        if any(kw in affil_lower for kw in NON_ACADEMIC_KEYWORDS) and not any(kw in affil_lower for kw in ACADEMIC_KEYWORDS):
            companies.append(affiliation)
            authors.append(name)
        if "@" in affiliation and not email:
            # Try to extract email
            words = affiliation.split()
            for word in words:
                if "@" in word:
                    email = word.strip(";,.()[]")
                    break

    return {
        "PubmedID": pmid,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Author(s)": ", ".join(authors),
        "Company Affiliation(s)": ", ".join(companies),
        "Corresponding Author Email": email
    }