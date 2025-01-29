```markdown
# Abstract Categorization and Session Assignment Tool

This Python script uses Google's Generative AI models to categorize research paper abstracts and assign them to sessions based on topic similarity and other criteria.
It reads abstract data from an Excel spreadsheet, processes it using the Generative AI API, and outputs the results to a new spreadsheet and an HTML file for easy viewing in a browser.

## Requirements

- Python 3.x
- Required Python packages:
  ```bash
  pip install google-generativeai pandas tkinter IPython webbrowser
  ```

## Setup

1. Clone the repository (or copy the script):  If you cloned the repository, navigate to the project directory.
2. Install dependencies: Run the command above to install the necessary Python packages.
3. Google Cloud API Key: Obtain a Google Cloud API key with access to the Generative AI API.  You'll be prompted to enter this key when running the script.
4. UI Assets: Ensure that the assets and pictures directories (containing the UI elements) are in the same directory as the Python script.  These are crucial for the UI to function correctly.  They should be structured like this:
AbstractCategorizationGCSM/
├── Progs/
│   └── Abstract_Categorization_working_with_Spreadsheet.py
│   └── assets/
│       └── frame0/
│           └── image_1.png
│           └── entry_1.png
│           └── ... (other UI elements)
│   └── pictures/
│       └── button_Small.png
└── ... (other files)

## Usage

1. Prepare your Excel spreadsheet: The spreadsheet should contain the following columns:
   - `Paper ID`
   - `Paper Title`
   - `Abstract`
   - `Authors`
   - `Country`
2. Run the script: Execute the Python script from your terminal:
   ```bash
   python Abstract_Categorization_working_with_Spreadsheet.py 
   ```
3. Model Selection: You'll be prompted to choose a Generative AI model (Gemini 1.5 Flash, Gemini Pro, etc.).  Note that access to some models might depend on your API key and region.
4. API Key Input: Enter your Google Cloud API key when prompted.
5. File Selection: A file dialog will open, allowing you to select your Excel spreadsheet.
6. Processing: The script will process the abstracts, categorize them, assign sessions, and save the results. This might take some time depending on the number of abstracts.
7. Output:
   - A new Excel file (with "_processed" appended to the original filename) will be created in the same directory, containing the categorized abstracts and session assignments.
   - An HTML file ("Sessions_schedule.html") will also be created, which will open in your default web browser for easy review of the schedule.
8. Session Re-evaluation (Optional): The script will ask if you want to re-evaluate the session assignments.  Choosing "Y" will run the re-evaluation process.
9. UI Interaction: The Tkinter UI will appear.
   - Terminal Box: The bottom box will display program output, including progress messages, errors, and information about actions performed.
   - Input Spreadsheet: Enter the path to your Excel spreadsheet in the text box or click the browse button to select it.
   - LLM Selection: Enter the name of the desired Large Language Model (LLM) from Google (e.g., gemini-1.5-flash, gemini-pro). Make sure you have access to the chosen model via your API key.
   - API Key Input: Enter your Google Cloud API key in the provided box.
   - Start Button: Click the "Start" button to begin the analysis.
   - Info Button: Click the info button for more information about the program and its creators.

## Functionality

- Abstract Categorization: Uses Generative AI to categorize abstracts based on predefined topics and sub-topics.  Identifies research methods, scope, and forecasted presentation time.
- Affiliation Search: Extracts affiliation information (organization, university) from the abstract, title, authors, and country.
- Session Assignment: Assigns abstracts to sessions based on topic similarity, group size limits (max 6 abstracts per group), and country diversity.
- Session Re-evaluation: Allows for re-evaluation and adjustment of session assignments.
- Spreadsheet Input/Output: Reads abstract data from an Excel spreadsheet and writes the processed results to a new spreadsheet.
- HTML Output: Generates an HTML file for easy viewing of the session schedule in a web browser.
- Tkinter UI: Provides a graphical user interface for easier interaction with the program.

## Notes

- Processing time can vary depending on the number of abstracts and the chosen Generative AI model.
- The script includes error handling for potential issues during abstract processing.
- Be sure to have a valid Google Cloud API key with appropriate access to the Generative AI models.
- The UI elements (images, etc.) are essential for the program to run correctly. Ensure they are placed in the correct directories as described in the setup instructions.
```
