
import os
import google.generativeai as genai
#import panda as pd

#Define method to categorize abstract
def categorize_abstract(abstract):
    #Setting up prompt
    prompt = f"""
    Please analyze the following abstract, decide which overall categories would best describe the abstract, decide the field of research that the abstract is targeting, identify the main research method that the abstract is addressing, analyze whether the research of the provide abstract will address a general topic (overview, theoretical framework, etc.) or a specific technical topic (applications, technical solutions, etc.), and forecast whether the presentation of the topic associated with the target abstract would be brief (less than 10 minutes) or long (up to 15 minutes) based on the information of the topic to be covered as described in the abstract. The answer for each part must be concise and should be up to 3 words.
    Abstract:
    {abstract}
    Response format:
    - Overall Category: Category name
    - Field of research: Field name
    - Research methods: Methodology
    - Scope: General or Specific 
    - Research Purpose: Theoretical or Applied
    - Forecasted Presentation Time: Brief or Standard
    """
    #Configure generative ai model and API key
    genai.configure(api_key="AIzaSyAoW91r6jsG5rsnrg4_0X8DeOAYPD94Nog")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    #Find the best fit category name from the response
    category_line1 = [line for line in response.text.split("\n") if line.startswith("- Overall Category: ")]
    if category_line1:
        overall_category = category_line1[0].split(": ")[1].strip()
    else:
        overall_category = "N/A"
    #Find the second best fit category name from the response
    category_line2 = [line for line in response.text.split("\n") if line.startswith("- Field of research: ")]
    if category_line2:
        research_field = category_line2[0].split(": ")[1].strip()
    else:
        research_field = "N/A"
    #Find the third best fit category name from the response
    category_line3 = [line for line in response.text.split("\n") if line.startswith("- Research methods: ")]
    if category_line3:
        research_method = category_line3[0].split(": ")[1].strip()
    else:
        research_method = "N/A"
    #Define Scope level
    category_line4 = [line for line in response.text.split("\n") if line.startswith("- Scope: ")]
    if category_line4:
        scope = category_line4[0].split(": ")[1].strip()
    else:
        scope = "N/A"
    #Distinguish whether the target paper is a theoretical or applied one
    category_line5 = [line for line in response.text.split("\n") if line.startswith("- Research Purpose: ")]
    if category_line5:
        purpose = category_line5[0].split(": ")[1].strip()
    else:
        purpose = "N/A"
    #Forecast presentation time needed for the abstract
    category_line6 = [line for line in response.text.split("\n") if line.startswith("- Forecasted Presentation Time: ")]
    if category_line6:
        forecasted_time = category_line6[0].split(": ")[1].strip()
    else:
        forecasted_time = "N/A"
    #Return values from method
    return overall_category, research_field, research_method, scope, purpose, forecasted_time

if __name__ == "__main__":
    while True:
        user_input = input ("Please provide abstract: ")
        if not user_input:
            print("No abstract provided. Cancelling request...")
            break
        overall_category, research_field, research_method, scope, purpose, forecasted_time = categorize_abstract(user_input)

        print("- Overall Category: ", overall_category)
        print("- Field of research: ", research_field)
        print("- Research methods: ", research_method)
        print("- Scope: ", scope)
        print("- Research Purpose: ", purpose)
        print("- Forecasted Presentation Time: ", forecasted_time)

        continue_input = input("Would you like to continue with another abstract? (y/n): ")
        if continue_input.lower() != "y":
            print("Exiting...")
            break
