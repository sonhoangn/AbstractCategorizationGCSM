import os
import pandas as pd
import google.generativeai as genai
import time
from tkinter import Tk, filedialog


def main():
  categories = [
      "Circular economy",
      "Energy efficiency",
      "Green supply chains",
      "Sustainable materials",
      "Digital manufacturing"
  ]

  # Asking for API key
  def get_api_key():
      """Prompts the user to enter their API key."""
      api_key = input("Enter your API key: ")
      return api_key

  def categorize_abstract(abstract):

      prompt = f"""
      I have an abstract related to sustainable manufacturing. Please assign it to one of the following categories or suggest a new one if necessary:

      Categories:
      {", ".join(categories)}

      Abstract:
      {abstract}

      Response format:
      - Assigned category: [Category name or ""Other - [short description]""]
      - Optional keywords: [keyword1, keyword2, keyword3] 
      """
      genai.configure(api_key=pak)
      model = genai.GenerativeModel("gemini-1.5-flash")
      response = model.generate_content(prompt)

      # Find the category in the response
      category_line = [line for line in response.text.split("\n") if line.startswith("- Assigned category: ")]
      if category_line:
          category = category_line[0].split(": ")[1].strip()
      else:
          category = "Other"

      # Extract keywords
      keywords = response.text.split("keywords: ")[1].strip().split(", ")[:3]

      # Get token counts
      prompt_tokens = model.count_tokens(prompt)
      response_tokens = model.count_tokens(response.text)

      return category, keywords, prompt_tokens, response_tokens

  def categorize_abstracts_from_excel(file_path):

      # Read the Excel file
      df = pd.read_excel(file_path)

      if "abstract" not in df.columns:
          print("The selected file must have a column named 'abstract'.")
          return None

      results = []
      for index, abstract in enumerate(df["abstract"]):
          if pd.isna(abstract):
              results.append(("N/A", "N/A", 0, 0))
              continue

          try:
              category, keywords, prompt_tokens, response_tokens = categorize_abstract(abstract)
              results.append((category, keywords, prompt_tokens, response_tokens))

              # Add a delay between requests to pace API calls
              time.sleep(1)  # Adjust the delay time as needed
          except Exception as e:
              print(f"Error processing abstract {index+1}: {e}")
              results.append(("Error", "Error", 0, 0))

      # Create a DataFrame with results
      df_results = pd.DataFrame(results, columns=["Selected Category", "Keywords", "Prompt Tokens", "Response Tokens"])

      return df_results

  # Open file dialog to select an Excel file
  root = Tk()
  root.withdraw()  # Hide the main Tkinter window
  file_path = filedialog.askopenfilename(
      title="Select an Excel file",
      filetypes=[("Excel files", "*.xlsx *.xls")]
  )
  root.destroy()

  if not file_path:
      print("No file selected.")
      return

  # Ensure `df` is defined before using it
  if file_path:
        pak = get_api_key()
        df = pd.read_excel(file_path)  # Read the Excel file again to create `df`

  # Categorize abstracts
  df_results = categorize_abstracts_from_excel(file_path)

  if df_results is None:
      return

  # Save the results to a new Excel file
  output_file = file_path.replace(".xlsx", "_categorized.xlsx")
  with pd.ExcelWriter(output_file, mode='w') as writer:
      df.to_excel(writer, sheet_name='Original Abstracts')
      df_results.to_excel(writer, sheet_name='Categorized Abstracts')

  print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()