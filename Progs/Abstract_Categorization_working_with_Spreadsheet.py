import os
import google.generativeai as genai
import pandas as pd
import time
from tkinter import Tk, filedialog

from pandas.io.formats.format import return_docstring

def main():
    #Asking for API key
    def get_api_key():
        """Prompts the user to enter their API key."""
        api_key = input("Enter your API key: ")
        return api_key
    #Define method to categorize abstract
    def categorize_abstract(abstract):
        #Setting up prompt
        prompt = f"""
        Analyze the following abstract, decide which overall categories (the overall categories must be chosen from one of the predefined topics) would best describe the abstract, decide the field of research (must be chosen from one of the sub-topics of the chosen predefined topic) that the abstract is targeting, identify the main research method that the abstract is addressing, analyze whether the research of the provide abstract will address a general topic (overview, theoretical framework, etc.) or a specific technical topic (applications, technical solutions, etc.), and forecast whether the presentation of the topic associated with the target abstract would be brief (less than 10 minutes) or long (up to 15 minutes) based on the information of the topic to be covered as described in the abstract. The answer for each part must be concise and should be up to 3 words. The response should also include the number of token for the prompt and the response for troubleshooting and billing purpose.
        Abstract:
        {abstract}
        Predefined topics and their sub-topics:
        1. Predefined Topic: Sustainable Materials & Products
        - Sub-topic: Low carbon materials and critical raw materials
        - Sub-topic: Material recycling
        - Sub-topic: Product design, redesign and innovation
        - Sub-topic: Product recovery, reuse and remanufacturing
        - Sub-topic: Product life cycle, information and knowledge management
        - Sub-topic: Life cycle assessment, risk assessment
        - Sub-topic: Sustainable business models
        2. Predefined Topic: Sustainable Manufacturing Processes:
        - Sub-topic: Manufacturing processes, tools and equipment
        - Sub-topic: Energy and resource efficiency
        - Sub-topic: Resource utilization and waste reduction
        - Sub-topic: Maintenance, repair and overhaul for machines and equipment
        3. Predefined Topic: Sustainable Manufacturing Systems:
        - Sub-topic: Manufacturing system design
        - Sub-topic: Simulation tools for manufacturing system design/layout testing
        - Sub-topic: Sustainable supply chain
        - Sub-topic: Data usage and sustainable manufacturing/production planning
        - Sub-topic: Metrics for sustainable manufacturing systems
        4. Predefined Topic: Crosscutting Topics:
        - Sub-topic: Industry 4.0 and sustainable manufacturing
        - Sub-topic: Circular economy
        - Sub-topic: CO2 neutral production
        - Sub-topic: Regional integration for sustainability
        - Sub-topic: Sustainable energy transition / Sustainable energy development
        - Sub-topic: Policy design for sustainability
        - Sub-topic: Engineering education towards sustainable development
        - Sub-topic: Regional integration of sustainability in South East Asia
        Response format:
        - Overall Category: Category name
        - Field of research: Field name
        - Research methods: Methodology
        - Scope: General or Specific 
        - Research Purpose: Theoretical or Applied
        - Forecasted Presentation Time: Brief or Standard
        - Prompt token count
        - Response token count
        """
        #Configure generative ai model using personal API key and define response
        #pak = get_api_key()
        genai.configure(api_key=pak)
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

        #Get token count
        prompt_tokens = str(model.count_tokens(prompt)).split(": ")[1].strip()
        response_tokens = str(model.count_tokens(response.text)).split(": ")[1].strip()
        #Return values from method
        return overall_category, research_field, research_method, scope, purpose, forecasted_time, prompt_tokens, response_tokens

    def input_from_spreadsheet(file_path):
        #Create data frame from the provided spreadsheet
        df = pd.read_excel(file_path)
        #Define response from genai as an array
        results = []
        #Check if abstract column present in the spreadsheet
        if "abstract" not in df.columns:
            print("Unable to locate abstracts list.")
            return None
        #Start prompting for each abstract
        for index, abstract in enumerate(df["abstract"]):
            #Check if abstract exists, if not then return n/a
            if pd.isna(abstract):
                results.append((index, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 0, 0))
            #If abstract exists, continue prompting with genai
            try:
                overall_category, research_field, research_method, scope, purpose, forecasted_time, prompt_tokens, response_tokens = categorize_abstract(abstract)
                results.append((index, abstract, overall_category, research_field, research_method, scope, purpose, forecasted_time, prompt_tokens, response_tokens))
                # Include a delay between prompt request
                time.sleep(3)
            #Define exception
            except Exception as e:
                print(f"Error processing abstract {index+1}: {e}")
                results.append((index, abstract, "Error", "Error", "Error", "Error", "Error", "Error", 0, 0))
        #Create a Data frame with results
        df_results = pd.DataFrame(results, columns=["No.", "Abstract", "Overall Category", "Field of research", "Research methods", "Scope", "Research Purpose", "Forecasted Presentation Duration", "Prompt token count", "Response token count"])

        return df_results

    if __name__ == "__main__":
        #Select a spreadsheet
        root = Tk()
        root.withdraw() # Hide the main Tkinter window
        file_path = filedialog.askopenfilename(
            title="Select Abstracts List",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        root.destroy()

        if not file_path:
            print("No file selected.")
            return

        if file_path:
            pak = get_api_key()
            df = pd.read_excel(file_path)

        df_results = input_from_spreadsheet(file_path)

        if df_results is None:
            return

        #Save data frame results to a new spreadsheet
        output_file = file_path.replace(".xlsx", "_processed.xlsx")
        with pd.ExcelWriter(output_file, mode='w') as writer:
            df_results.to_excel(writer, sheet_name='Processed')

        print(f"Results are saved to {output_file}")

if __name__ == "__main__":
    main()