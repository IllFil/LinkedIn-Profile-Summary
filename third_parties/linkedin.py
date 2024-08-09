import os
import requests
import json

def clean_data(data):
    """Recursively remove all null values, empty lists, and empty dictionaries from the JSON data."""
    if isinstance(data, dict):
        # Recursively clean the values in the dictionary
        cleaned_dict = {k: clean_data(v) for k, v in data.items() if v is not None}
        # Remove empty dictionaries
        return {k: v for k, v in cleaned_dict.items() if v or v == 0 or v is False}
    elif isinstance(data, list):
        # Recursively clean items in the list
        cleaned_list = [clean_data(item) for item in data if item is not None]
        # Remove empty lists
        return [item for item in cleaned_list if item or item == 0 or item is False]
    else:
        # Return the value if it is not null
        return data

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )

    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"linkedin_profile_url": linkedin_profile_url,
                    'extra': 'exclude',
                    'github_profile_id': 'include',
                    'facebook_profile_id': 'include',
                    'twitter_profile_id': 'include',
                    'personal_contact_number': 'include',
                    'personal_email': 'include',
                    'inferred_salary': 'include',
                    'skills': 'include',
                    'use_cache': 'if-present',
                    'fallback_to_cache': 'on-error',
                    },
            headers=header_dic,
            timeout=10,
        )

    data = response.json()

    cleaned_data = clean_data(data)

    return cleaned_data
