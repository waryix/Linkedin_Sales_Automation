# ai_core.py (Final Version with Cleaner Prompt)

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def generate_personalized_message(profile_text: str, campaign_details: dict) -> str:
    """
    Generates a personalized message using a ReAct-style prompt.
    """
    prompt = f"""
    Your task is to act as an expert B2B Sales Development Representative (SDR). You will draft a hyper-personalized LinkedIn connection request message.

    **Campaign Details:**
    - Product/Service: {campaign_details['product_description']}
    - Target Industry: {campaign_details['target_industry']}
    - Ideal Job Roles: {campaign_details['ideal_job_roles']}
    - Outreach Goal: {campaign_details['outreach_goal']}
    - Brand Voice: {campaign_details['brand_voice']}

    **Prospect's Raw LinkedIn Profile Text:**
    ---
    {profile_text}
    ---

    **Your Thought Process (Follow these steps):**
    1.  **Filter the Noise:** The raw text above is messy and contains irrelevant data, navigation links, and code from the webpage. IGNORE all of this noise. Focus ONLY on the human-written content that belongs to the user's profile (like their name, headline, summary/about section, experience descriptions, and posts).
    2.  **Analyze the Hook:** From the clean, relevant profile text you filtered, identify the single most compelling and unique piece of information to use as a personalized hook. This could be a recent post, a specific achievement, a shared interest, or a volunteer activity.
    3.  **Connect to Value:** Briefly explain how the hook you found relates to the product/service you are offering.
    4.  **Draft the Message:** Based on the hook and value connection, write a short, concise, and compelling connection message. The message MUST be under 300 characters. Adhere strictly to the requested '{campaign_details['brand_voice']}' brand voice.
    5.  **Final Output:** Present your final answer ONLY as a valid JSON object. Do not include any text or markdown before or after the JSON.

    **Example Output Format:**
    {{
      "thought_process": "The user recently posted about the challenges of onboarding new remote hires. This is a perfect hook because our product directly solves that problem by automating the process.",
      "personalized_message": "Hi [Name], saw your post on remote onboarding challenges. My company helps HR teams automate that process. Thought you might find it interesting."
    }}

    **Now, generate the output for the provided profile and campaign.**
    """

    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
        return cleaned_response
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f'{{"error": "Failed to generate message", "details": "{e}"}}'