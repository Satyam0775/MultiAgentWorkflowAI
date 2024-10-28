import requests
import pandas as pd

# Set your SerpAPI key
API_KEY = ""
BASE_URL = "https://serpapi.com/search"

def research_company(company_name):
    """Search for company information using SerpAPI."""
    params = {
        "engine": "google",
        "q": f"{company_name} company overview",
        "api_key": API_KEY,
        "num": 10  # Number of results to return
    }
    
    # Perform the search using SerpAPI
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extracting relevant information
        results = []
        for item in data.get("organic_results", []):
            title = item.get("title")
            link = item.get("link")
            snippet = item.get("snippet")
            results.append({"Title": title, "Link": link, "Snippet": snippet})
        
        return results
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def identify_key_offerings():
    """Identify key offerings and focus areas."""
    key_offerings = [
        "Consulting Services",
        "Audit Services",
        "Tax Advisory",
        "Risk Management",
        "Financial Advisory",
        "Technology Implementation"
    ]
    
    focus_areas = [
        "Operations",
        "Supply Chain Management",
        "Customer Experience",
        "Digital Transformation",
        "Sustainability",
        "Cybersecurity"
    ]
    
    return key_offerings, focus_areas

def save_results_to_csv(results, company_name):
    """Save research results to a CSV file."""
    df = pd.DataFrame(results)
    filename = f"{company_name}_research_results.csv"
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")
    return filename

if __name__ == "__main__":
    company_name = "Deloitte"
    
    print(f"Researching {company_name}...")
    results = research_company(company_name)
    
    if results:
        print(f"\nResearch results for {company_name}:")
        for i, item in enumerate(results):
            print(f"{i + 1}: {item['Title']} - {item['Link']}")
            print(f"Snippet: {item['Snippet']}\n")
        
        key_offerings, focus_areas = identify_key_offerings()
        
        print(f"\nKey Offerings of {company_name}:")
        for offering in key_offerings:
            print(f"- {offering}")
        
        print(f"\nStrategic Focus Areas of {company_name}:")
        for area in focus_areas:
            print(f"- {area}")
        
        # Save results to CSV
        save_results_to_csv(results, company_name)
