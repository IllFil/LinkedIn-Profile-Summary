# LinkedIn Profile Summary Generator

## Overview

This project is designed to extract and summarize LinkedIn profiles making serch by name using LLM llama3.1 and tavily for internet access . It integrates several components including LinkedIn profile scraping, natural language processing (NLP) for generating summaries, and a Flask web service for user interaction.

## Components

1. **LinkedIn Profile Lookup and Summary Generation**:
   - **Function:** `look_up_person(name: str) -> Tuple[Summary, str]`
   - **Description:** 
     - **Step 1:** Finds the LinkedIn profile URL using `get_profile_url_tavily(name: str)`.
     - **Step 2:** Scrapes LinkedIn profile data from the found URL.
     - **Step 3:** Generates a concise summary of the person's qualifications and experience using the `llama3.1` model.
   - **Dependencies:** `langchain`, `langchain_ollama`, `third_parties.linkedin`

2. **LinkedIn Profile URL Lookup**:
   - **Function:** `get_profile_url_tavily(name: str) -> str`
   - **Description:** 
     - Uses the Tavily API to search for a LinkedIn profile page based on the person's name.
     - Retrieves the LinkedIn profile URL from the search results.
   - **Dependencies:** `TavilySearchResults`
   - **Implementation:**
     ```python
     def get_profile_url_tavily(name: str):
         """Searches for LinkedIn Profile Page."""
         search = TavilySearchResults()
         res = search.run(f"{name}")
         return res[0]["url"]
     ```

3. **Flask Web Service**:
   - **Routes:**
     - `/` - Displays the main page.
     - `/process` - Processes a POST request containing a person's name, retrieves and summarizes their LinkedIn profile, and returns the summary as JSON.
   - **Dependencies:** `Flask`, `person_summary`

4. **Data Cleaning and Scraping**:
   - **Function:** `scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False)`
   - **Description:** Scrapes LinkedIn profile data and cleans the JSON response.
   - **Dependencies:** `requests`, `json`
