# Abstract Categorization and Session Assignment Tool

This Python program uses Google's Generative AI models to categorize research paper abstracts and assign them to sessions based on topic similarity and other criteria.
It reads abstract data from an Excel spreadsheet, processes it using the Generative AI API, and outputs the results to a new spreadsheet and an HTML file for easy viewing in a browser.

## Requirements

```markdown
- Python 3.x
- Required Python packages: check requirements.txt in Progs for all necessary packages to be installed in order to use this program.
  ```

## Setup

1. Clone the repository (or copy the program):  If you cloned the repository, navigate to the project directory.
2. Install dependencies: Run the command below to install all necessary Python packages.
  ```markdown
  pip install -r requirements.txt
  ```
4. Google Cloud API Key: Obtain a Google Cloud API key with access to the Generative AI API.  You'll be prompted to enter this key when running the program.
5. UI Assets: Ensure that the assets folder (containing all UI elements) is in the same directory as the Python program.  These are crucial for the UI to function correctly.
   
## Usage

1. Prepare your Excel spreadsheet: The spreadsheet must contain at least the following columns:
   - `Paper ID`
   - `Paper Title`
   - `Abstract`
   - `Authors`
   - `Country`
2. Run the program: Execute the Python program Main_Application_UI.py or run the following command in your terminal:
   ```bash
   python Main_Application_UI.py 
   ```
3. The UI has different areas to input necessary information: "API Key", "Model Selection" and "Input Spreadsheet". 
4. API Key: Enter your Google Cloud API key, hit the blue tick button located on the right of the text box to save the provided API Key.
5. Model Selection: You can select your desired model from a drop-down list containing different values: Gemini 1.5 Flash, Gemini 1.5 Pro, Gemini 2.0 Flash, etc. Similar to the previous item, you must press the button on the right to save your selection. Note that access to some models might depend on your API key and region.
7. Input Spreadsheet: Do not input directly in the textbox and instead press the blue button on the right. A file dialog will open, allowing you to select your Excel spreadsheet. As you select your file, the path to the provided data will be saved automatically.
8. Processing: After providing all necessary data, you could proceed with pressing the "START" button. The program would automatically start processing the provided list of abstracts, categorizing them and assigning sessions. The. This might take some time depending on the number of abstracts.
9. Output:
   - A new Excel file (with "_processed_<name of the chosen LLM>" appended to the original filename) will be created in the same directory of the original spreadsheet file, containing the categorized abstracts and session assignments.
   - An HTML file ("Sessions_schedule_<name of the chosen LLM>.html") will also be created in the "Results" folder located in the temporary directory in your C Drive, which will open in your default web browser for easy review of the schedule. Refer to the output messages printed on the terminal to locate the html file should you need to retrieve it.
10. Refine function (Optional): As you click the "REFINE" button, you will be prompted to select an already processed list of abstracts (Abstracts that have been processed and assigned with session no.). Upon selecting the required list, the program will attempt to go through the provided list to merge any small sessions into sessions of 6 items each.
11. Other UI Interactions:
   - Terminal Box: The bottom box will display program output, including progress messages, errors, and information about actions performed.
   - Processing Duration (s): This little information box will display the total time (in seconds) taken to complete the entire abstracts processing routine.
   - Info Button: Click the info button for more information about the program, its creators and to reveal the link to the program's repository on github for all source codes.

## Functionality

- Abstract Categorization: Uses Generative AI to categorize abstracts based on predefined topics and sub-topics.  Identifies research methods, scope, and forecasted presentation time.
- Session Assignment: Assigns abstracts to sessions based on topic similarity, group size limits (max 6 abstracts per group), and country diversity.
- Session Splitting: Splitt any sessions with more than 6 items to smaller sessions.
- Session Merge: Merge smaller sessions into sessions with exactly 6 items.
- Spreadsheet Input/Output: Reads abstract data from an Excel spreadsheet and writes the processed results to a new spreadsheet.
- HTML Output: Generates an HTML file for easy viewing of the session schedule in a web browser.
- Tkinter UI: Provides a graphical user interface for easier interaction with the program.

## Notes

- Processing time can vary depending on the number of abstracts and the chosen Generative AI model.
- The program includes error handling for potential issues during abstract processing.
- Be sure to have a valid Google Cloud API key with appropriate access to the Generative AI models.
- The UI elements (images, etc.) are essential for the program to run correctly. Ensure they are placed in the correct directories as described in the setup instructions.
- Ensure the source spreadsheet to be provided to the program need to contain the required column as aforementioned in the Usage section, else it would encounter error as soon as the "START" button is pressed.
- In case you have any issues with the program or any questions, kindly send me an email at:
```markdown
  sonhoangn@yahoo.com
```
