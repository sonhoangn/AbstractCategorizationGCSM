#Google.generativeai is required to setup interaction with various generative ai models from google.
import google.generativeai as genai
#Pandas is required to work with Data frame (Create data frame from spreadsheet, turn lists, arrays into data frames). DF is a form of machine-readable item, which make it easier to analyze.
import pandas as pd
import time
#TKinter library helps with setting up pop-up dialogues and menus
from tkinter import Tk, filedialog
#This library is used to help display information onto browsers in HTML format
from IPython.display import HTML, display
import webbrowser
import os
import tempfile

def main():
    #Generative AI models selection. Only 2 of them are actually usable for a free public API key from google
    def model_select():
        print("Please choose a model:")
        print("1. Gemini-1.5-flash")
        print("2. Gemini-2.0-flash-experimental (Check if your API key and region can access this model before choosing)")
        print("3. Gemini Pro")
        print("4. Gemini Ultra (Check if your API key and region can access this model before choosing)")
        print("5. PaLM 2 (Check if your API key and region can access this model before choosing)")
        model_choice = input("You have selected model (1/2/3/4/5): ")
        if model_choice == "1":
            return "gemini-1.5-flash"
        elif model_choice == "2":
            return "gemini-2.0-flash"
        elif model_choice == "3":
            return "gemini-pro"
        elif model_choice == "4":
            return "gemini-ultra"
        elif model_choice == "5":
            return "palm-2"
        else:
            print("Invalid model selection. Default model shall be used: gemini-1.5-flash")
            return "gemini-1.5-flash"

    #Asking for API key
    def get_api_key():
        api_key = input("Enter your API key: ")
        return api_key

    #Define method to categorize abstract
    def categorize_abstract(index, abstract):
        #Setting up prompt
        prompt = f"""
        Analyze the following abstract, decide which overall categories (the overall categories must be chosen from one of the 4 predefined topics) would best describe the abstract, decide the field of research (must be chosen from one of the sub-topics of the chosen predefined topic) that the abstract is targeting, identify the main research method that the abstract is addressing, decide the scope of the abstract based on the provided info by choosing a score between 1 to 6 (with 1 being extremely narrow scope and 6 being extremely broad scope), and forecast whether the presentation of the topic associated with the target abstract would be brief (less than 10 minutes) or long (up to 15 minutes) based on the information of the topic to be covered as described in the abstract. The answer for Overall Category must be strictly chosen only from the list of 4 predefined topics (do not generate new topics that is not the same as the 4 predefined topics), and must be cleaned, free of any extra special characters. The answer for Field of research must be strictly chosen from the list of subtopics (do not generate new topics that is not the same as the provided subtopics), and must be cleaned, free of any extra special characters. The answer for other part must be concise and no longer than 3 words. The response should also include the number of token for the prompt and the response for troubleshooting and billing purpose.
        Paper index:
        {index}
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
        - Scope: Score Number between 1 to 6
        - Research Purpose: Theoretical or Applied
        - Forecasted Presentation Time: Brief or Standard
        - Prompt token count
        - Response token count
        """
        #Configure generative ai response
        response = model.generate_content(prompt)
        #Find the best fit overall category name from the response
        line1 = [line for line in response.text.split("\n") if line.startswith("- Overall Category: ")]
        if line1:
            overall_category = line1[0].split(": ")[1].strip()
        else:
            overall_category = "N/A"
        #Find the best fit topic name from the response
        line2 = [line for line in response.text.split("\n") if line.startswith("- Field of research: ")]
        if line2:
            research_field = line2[0].split(": ")[1].strip()
        else:
            research_field = "N/A"
        #Find the best fit research method name from the response
        line3 = [line for line in response.text.split("\n") if line.startswith("- Research methods: ")]
        if line3:
            research_method = line3[0].split(": ")[1].strip()
        else:
            research_method = "N/A"
        #Define Scope level
        line4 = [line for line in response.text.split("\n") if line.startswith("- Scope: ")]
        if line4:
            scope = line4[0].split(": ")[1].strip()
        else:
            scope = "N/A"
        #Distinguish whether the target paper is a theoretical or applied one
        line5 = [line for line in response.text.split("\n") if line.startswith("- Research Purpose: ")]
        if line5:
            purpose = line5[0].split(": ")[1].strip()
        else:
            purpose = "N/A"
        #Forecast presentation duration needed for the abstract
        line6 = [line for line in response.text.split("\n") if line.startswith("- Forecasted Presentation Time: ")]
        if line6:
            forecasted_time = line6[0].split(": ")[1].strip()
        else:
            forecasted_time = "N/A"

        #Get token count
        prompt_tokens = str(model.count_tokens(prompt)).split(": ")[1].strip()
        response_tokens = str(model.count_tokens(response.text)).split(": ")[1].strip()
        #Return values from method
        return overall_category, research_field, research_method, scope, purpose, forecasted_time, prompt_tokens, response_tokens

    #Search for affiliation
    def affiliation_search(index, abstract, paper_title, authors_list, nation):
        prompt_2 = f"""Based on the paper tile, list of authors, its abstract and the nation name. Extract the name of the organization, university, research institutions, etc. that published this research paper (the name of the organization is usually associated with the first author, and would be contained in parentheses next to the name of the first author for every abstract). The answer must be clean, clear of any special character, and should be no more than 5 words (names of the organization can be in the form of an abbreviation).
        Paper index:
        {index}
        Abstract
        {abstract}
        Paper Title:
        {paper_title}
        Authors List:
        {authors_list}
        Nation:
        {nation}
        Response format:
        - Affiliation: Name of the organization (can not be N/A)
        """
        #Configure generative ai response
        response_2 = model.generate_content(prompt_2)
        #Extract the target organization name from Gen AI's response
        line7 = [line for line in response_2.text.split("\n") if line.startswith("- Affiliation: ")]
        if line7:
            affiliation_org = line7[0].split(": ")[1].strip()
        else:
            affiliation_org = "N/A"
        #Assign nation
        affiliation_country = nation
        return affiliation_org, affiliation_country

    def session_assignment(df_results):
        columns_to_analyze = ['No.', 'Overall Category', 'Topic', 'Organization', 'Country']
        df_selected_column = df_results[columns_to_analyze]
        prompt_3=f"""Analyze the provided data table containing a list of abstracts with associated information including organizations, countries, topic, and overall category:
        1. Strict rule: Group Size Limit
        1a. Each group MUST contain no more than 6 abstracts
        1b. Analyze the abstracts within that group based on their topic (highest priority) and overall category (second highest priority)
        1c. If a group exceeds 6 abstracts, redistribute the abstracts into smaller groups, ensuring no group exceeds 6 abstracts
        2. Strict rule: Minimum Number of Groups
        2a. The number of groups MUST be sufficient to accommodate all abstracts while adhering to the 6-abstract limit
        2b. Example: If there are 60 abstracts, there must be at least 10 groups (60 abstracts / 6 abstracts per group = 10 groups).
        3. Strict rule: Group Similarity: Abstracts within the same group MUST exhibit high similarity in topic (highest priority) and overall category (second highest priority).
        4. Optional rule: Country Diversity: Whenever possible, ensure each group contains abstracts from diverse countries.
        5. Present your answer for each abstract in the following format: 
        5a. Abstract number [index number] belongs to group: [group number]. 
        5b. Start with group number 1 and increment sequentially.
        5c. Example: 
        Abstract number 1 belongs to group: 1
        Abstract number 23 belongs to group: 2
        
        Data table to be analyzed:
        {df_selected_column.to_markdown(index=False)}
        Response format:
        - Abstract number belongs to group number: group number"""
        response_3 = model.generate_content(prompt_3)
        # Define an array containing session numbers
        session_numbers = []
        lines = response_3.text.split("\n")

        for line in lines:
            if line.startswith("- "):
                try:
                    session_number = line.split(": ")[1].strip()
                    session_numbers.append(session_number)
                except IndexError:
                    session_numbers.append("N/A")
        result = pd.DataFrame(session_numbers, columns=["Session No."])
        #Turn this thing on in case debug is required
        #print(result)
        print("Session assignment completed...")
        return result

    # Session assignment Reevaluation
    def session_assignment_reevaluation(df_results):
        column_to_check = ['Paper Title', 'Topic', 'Overall Category', 'Session No.']
        df_reeval = df_results[column_to_check]
        prompt_3 = f"""Based on the data in the "Session No.", "Topic", and "Overall Category" columns, re-evaluate and adjust the "Session No." assignments for each abstract according to the following rules:
        1. Strict Rule: Response Format
        1a. The response format MUST strictly adhere to the following:
            - "Abstract number [index number] belongs to session number: [session number]"
        2. Rule: Minimum Number of Sessions
        2a. Calculate the minimum required number of sessions based on the total number of abstracts (minimum number of sessions = total abstracts / 6).
        2b. If the actual number of sessions in the data is less than the minimum required number:
            - Identify sessions with more than 6 abstracts.
            - Create new sessions by moving abstracts from these overcrowded sessions.
            - Ensure no session exceeds 6 abstracts after the adjustments.
        3. Rule: Session Size Limit        
        3a. If a session has more than 6 abstracts:
            - Analyze the abstracts within that session based on their "Topic" and "Overall Category" (prioritize "Topic").
            - Redistribute the abstracts into smaller sessions, ensuring no session exceeds 6 abstracts.
        4. Rule: Maintain Small Sessions
        4a. If a session has less than 6 abstracts, its assignments remain unchanged.
        5. Rule: No Maximum Session Limit        
        5a. The number of sessions is flexible and can increase as needed to accommodate all abstracts while adhering to the 6-abstract limit per session.
        6. Rule: Preserve Accurate Assignments        
        6a. If the existing "Session No." assignments are already accurate and compliant with all rules, maintain the original assignments.
        7. Output:        
        7a. Provide a list of adjusted "Session No." assignments for each abstract in the specified response format.
        7b. Example:
            - Abstract number 1 belongs to session number: 1
            - Abstract number 23 belongs to session number: 2
        Data table to be analyzed:
        {df_reeval.to_markdown(index=False)}
        Response format:
        - Abstract number belongs to session number: session number"""
        #Turn this thing on in case debugging is required
        #print(prompt_3)
        response_3 = model.generate_content(prompt_3)
        # Turn this thing on in case debugging is required. The response from the generative ai model might not always follow the same response format unless the rules explicitly state that the response should strictly follow the predefined response format.
        #print(response_3.text)
        # Define an array containing session numbers
        session_numbers = []
        lines = response_3.text.split("\n")

        for line in lines:
            if line.startswith("- "):
                try:
                    session_number = line.split(": ")[1].strip()
                    session_numbers.append(session_number)
                except IndexError:
                    session_numbers.append("N/A")
        result = pd.DataFrame(session_numbers, columns=["Session No."])
        # Turn this thing on in case debugging is required
        #print(result)
        print("New session schedule is provided...")
        return result

    def input_from_spreadsheet(file_path):
        #Create data frame from the provided spreadsheet
        df = pd.read_excel(file_path)
        #Record start time
        start_time = time.time()
        #Define response from genai as an array
        results = []
        #Check if abstract column present in the spreadsheet
        if "Abstract" not in df.columns:
            print("Unable to locate abstracts list.")
            return None
        #Start prompting for each abstract
        for index, row in df.iterrows():
            paper_title = row["Paper Title"]
            abstract = row["Abstract"]
            authors_list = row["Authors"]
            nation = row["Country"]
            #If abstract exists, continue prompting with genai
            try:
                overall_category, research_field, research_method, scope, purpose, forecasted_time, prompt_tokens, response_tokens = categorize_abstract(index, abstract)
                time.sleep(6)
                affiliation_org, affiliation_country = affiliation_search(index, abstract, paper_title, authors_list, nation)
                results.append((index, abstract, overall_category, research_field, research_method, scope, purpose, forecasted_time, affiliation_org, affiliation_country, prompt_tokens, response_tokens))

                # Print progress message every 10 abstracts
                if (index + 1) % 10 == 0:
                    print(f"No. of abstracts processed: {index + 1}")
                # Include a delay between prompt request
                time.sleep(6)
            #Define exception
            except Exception as e:
                print(f"Error processing abstract {index+1}: {e}")
                results.append((index, abstract, "Error", "Error", "Error", "Error", "Error", "Error", "Error", "Error", 0, 0))
        # Calculate and print total processing time
        print(f"All {index + 1} abstracts processed in {(time.time()-start_time):.2f} seconds.")
        #Create a Data frame with results
        df_results = pd.DataFrame(results, columns=["No.", "Abstract", "Overall Category", "Topic", "Research methods", "Scope", "Research Purpose", "Forecasted Presentation Duration", "Organization", "Country", "Prompt token count", "Response token count"])
        return df_results

    #Write results to spreadsheet
    def write_to_excel(df_results):
        columns_to_save = ['Paper ID', 'Session No.', 'Paper Title', 'Overall Category', 'Topic', 'Authors', 'Country']
        df_final = df_results[columns_to_save]
        # Save data frame results to a new spreadsheet
        output_file = file_path.replace(".xlsx", "_processed.xlsx")
        with pd.ExcelWriter(output_file, mode='w') as writer:
            df_final.to_excel(writer, sheet_name='Processed')
        print(f"Results are saved to {output_file}")
        browser_display(df_final)

    #Ask user whether they would like to have another sessions schedule
    def decision_to_evaluate(session_no, df_results):
        reevaluate_decision = input("Would you like another suggestion for session schedule? (Y/N): ").upper()
        if reevaluate_decision == 'Y':
            session_no = session_assignment_reevaluation(df_results)
            df_results['Session No.'] = session_no['Session No.']
            write_to_excel(df_results)
            return True
        else:
            print("Session scheduling is now completed, exiting...")
            return False

    def unexpected_characters(text):
        return text.replace('\u01b0', 'L')

    #Display results via browser
    def browser_display(df_final):
        output_path = "G:/GPE/GPE Projects/data/Browserdisplay/my_dataframe.html"
        html_table = df_final.to_html(index=False)
        html_table = unexpected_characters(html_table)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_table)

        try:
            webbrowser.open(output_path)
            print(f"DataFrame displayed in browser: {output_path}")
        except Exception as e:
            print(f"Error opening HTML file in browser: {e}")

    if __name__ == "__main__":
        #Select a spreadsheet
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select Abstracts List",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        root.destroy()

        #Check if a spreadsheet containing data has been selected
        if not file_path:
            print("No file selected.")
            return

        if file_path:
            #Setting up Generative AI model
            pak = get_api_key()
            gam = model_select()
            genai.configure(api_key=pak)
            model = genai.GenerativeModel(gam)

        #Transforming original spreadsheet into machine-readable data frame
        df = pd.read_excel(file_path)
        df1 = pd.DataFrame(df, columns=["Paper ID", "Paper Title", "Abstract", "Authors", "Country"])

        #Preliminary data processing using original spreadsheet data
        df_results = input_from_spreadsheet(file_path)

        if df_results is None:
            return
        time.sleep(5)

        #Preliminary session assignment based on preliminary data processing
        session_no = session_assignment(df_results)

        #Preparing final data in order to have them exported into the target human-readable spreadsheet
        df_results["Session No."] = session_no
        df_results["Paper Title"] = df1[['Paper Title']]
        df_results["Paper ID"] = df1[['Paper ID']]
        df_results["Authors"] = df1[['Authors']]

        #Write results to spreadsheet
        write_to_excel(df_results)

        #Check if users still want to have a different sessions schedule
        e_d = True
        while e_d:
            e_d = decision_to_evaluate(session_no,df_results)

if __name__ == "__main__":
    main()