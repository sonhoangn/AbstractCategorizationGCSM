
import os
import google.generativeai as genai
#import panda as pd

#Define method to categorize abstract
def categorize_abstract(abstract):
    #Setting up prompt
    prompt = f"""
    Please analyze the following abstract, decide which categories would best describe the abstract in 3 different priorities, and analyze whether the research of the provide abstract will address a general topic (overview, theoretical framework, etc.) or a specific technical topic (applications, technical solutions, etc.). The category name must be concise and should be up to 3 words.
    Abstract:
    {abstract}
    Response format:
    - Best fit category name: Category name
    - Second best fit category name: Category name
    - Third best fit category name: Category name
    - Topic: General or Specific - Theoretical or Application
    """
    #Configure generative ai model and API key
    genai.configure(api_key="AIzaSyAoW91r6jsG5rsnrg4_0X8DeOAYPD94Nog")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    #Find the best fit category name from the response
    category_line1 = [line for line in response.text.split("\n") if line.startswith("- Best fit category name: ")]
    if category_line1:
        category_best = category_line1[0].split(": ")[1].strip()
    else:
        category_best = "N/A"
    #Find the second best fit category name from the response
    category_line2 = [line for line in response.text.split("\n") if line.startswith("- Second best fit category name: ")]
    if category_line2:
        category_2ndbest = category_line2[0].split(": ")[1].strip()
    else:
        category_2ndbest = "N/A"
    #Find the third best fit category name from the response
    category_line3 = [line for line in response.text.split("\n") if line.startswith("- Third best fit category name: ")]
    if category_line3:
        category_3rdbest = category_line3[0].split(": ")[1].strip()
    else:
        category_3rdbest = "N/A"
    #Define topic level
    category_line4 = [line for line in response.text.split("\n") if line.startswith("- Topic: ")]
    if category_line4:
        topic = category_line4[0].split(": ")[1].strip()
    else:
        topic = "N/A"
    #Return values from method
    return category_best, category_2ndbest, category_3rdbest, topic

if __name__ == "__main__":
    while True:
        user_input = input ("Please provide abstract: ")
        if not user_input:
            print("No abstract provided. Cancelling request...")
            break
        category_best, category_2ndbest, category_3rdbest, topic = categorize_abstract(user_input)

        print("- Best fit category name: ", category_best)
        print("- Second best fit category name: ", category_2ndbest)
        print("- Third best fit category name: ", category_3rdbest)
        print("- Topic: ", topic)

        continue_input = input("Would you like to continue with another abstract? (y/n): ")
        if continue_input.lower() != "y":
            print("Exiting...")
            break
