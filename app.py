import os
import requests
import pandas as pd
import streamlit as st

# Set API keys
os.environ['OPENAI_API_KEY'] = 'AIzaSyC8tIrUlJcCRnyksbykluUZVvER6ynHQeI'
os.environ['SERPAPI_API_KEY'] = '533b5ecf4f322a3e1fb6c6341fc922267805add7e804f7783949a17175ed2f69'

# Define the directory to save CSV files
SAVE_DIR = r'C:\Users\satya\DeloitteResearchAgent'  # Absolute directory to save CSV files
os.makedirs(SAVE_DIR, exist_ok=True)  # Create directory if it doesn't exist

def industry_research(company_name, industry_name):
    """Fetch AI trends and use cases for the specified company and industry."""
    query_trends = f"{company_name} {industry_name} AI trends"
    query_use_cases = f"{company_name} {industry_name} AI use cases"
    
    params = {
        "api_key": os.environ['SERPAPI_API_KEY'],
        "q": query_trends,
        "num": 5
    }
    
    response_trends = requests.get("https://serpapi.com/search.json", params=params)
    if response_trends.status_code == 200:
        trends_results = response_trends.json().get('organic_results', [])
    else:
        trends_results = {"error": response_trends.text}
    
    params['q'] = query_use_cases  # Update query for use cases
    response_use_cases = requests.get("https://serpapi.com/search.json", params=params)
    if response_use_cases.status_code == 200:
        use_cases_results = response_use_cases.json().get('organic_results', [])
    else:
        use_cases_results = {"error": response_use_cases.text}
    
    return trends_results, use_cases_results

def summarize_trends(trends_results):
    """Summarize industry trends from the search results."""
    trends = []
    for result in trends_results:
        title = result.get('title')
        link = result.get('link')
        description = f"{title} can be explored further at [this link]({link})."
        trends.append({"Title": title, "Link": link, "Description": description})
    return trends

def propose_use_cases(use_cases_results):
    """Propose use cases based on search results."""
    use_cases = []
    for result in use_cases_results:
        title = result.get('title')
        link = result.get('link')
        description = f"Consider implementing: {title}. More details can be found at [this link]({link})."
        use_cases.append({"Title": title, "Link": link, "Description": description})
    return use_cases

def save_results_to_csv(findings, company_name):
    """Save the findings to a CSV file and return the filename."""
    df = pd.DataFrame(findings)
    filename = os.path.join(SAVE_DIR, f"{company_name}_research_results.csv")  # Save to the specified directory
    df.to_csv(filename, index=False)
    return filename

def main():
    st.title("Multi-Agent Workflow for AI Use Cases")

    # Input fields for company and industry
    company_name = st.text_input("Enter the Company Name", "Deloitte")
    industry_name = st.text_input("Enter the Industry Name", "Supply Chain Optimization")

    if st.button("Research"):
        if company_name and industry_name:
            # Conduct industry research
            trends_results, use_cases_results = industry_research(company_name, industry_name)
            
            # Display results
            if 'error' not in trends_results and 'error' not in use_cases_results:
                st.subheader(f"Industry Trends for {company_name} in {industry_name}:")
                trends = summarize_trends(trends_results)
                for trend in trends:
                    st.write(trend["Description"])

                # Propose Use Cases Section
                st.subheader("Proposed Use Cases")
                use_cases = propose_use_cases(use_cases_results)
                for i, use_case in enumerate(use_cases):
                    st.write(f"{i + 1}. Use Case {i + 1}: {use_case['Description']}")

                # Resource Links Section
                st.subheader("Resource Links")
                for result in trends_results + use_cases_results:
                    st.write(f"- [Resource: {result.get('title')}]({result.get('link')})")
                
                # Save results to CSV
                combined_findings = trends + use_cases  # Combine both findings
                csv_filename = save_results_to_csv(combined_findings, company_name)
                st.success(f"Results saved to {csv_filename} in the directory '{SAVE_DIR}'.")

            else:
                st.error("Error: " + (trends_results.get('error') or use_cases_results.get('error')))
        else:
            st.warning("Please enter both a company name and an industry name.")

if __name__ == "__main__":
    main()
