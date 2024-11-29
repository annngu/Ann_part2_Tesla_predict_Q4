import requests
import pdfplumber
import pandas as pd

# https://ir.tesla.com/#quarterly-disclosure
#Download the PDF file
pdf_url = "https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q1-2024-Update.pdf"
pdf_file_path = "TSLA-Q1-2024-Update.pdf"

response = requests.get(pdf_url)
with open(pdf_file_path, "wb") as f:
    f.write(response.content)
    
#Function to make column names unique
def make_unique_columns(columns):
    seen = {}
    unique_columns = []
    for col in columns:
        if col in seen:
            seen[col] += 1
            unique_columns.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            unique_columns.append(col)
    return unique_columns

#  Extract tables from the PDF
tables = []
with pdfplumber.open(pdf_file_path) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        page_tables = page.extract_tables()
        for table in page_tables:
            # Convert each table to a DataFrame
            df = pd.DataFrame(table[1:], columns=table[0])  # Use first row as column headers
            
            # Ensure unique column names
            df.columns = make_unique_columns(df.columns)
            
            # Append the DataFrame to the list
            tables.append(df)

# Combine all tables into one DataFrame (optional, if multiple tables are related)
all_tables_df = pd.concat(tables, ignore_index=True)

# Save to CSV
csv_file_path = "tesla_q1_2024.csv"
all_tables_df.to_csv(csv_file_path, index=False)

print(f"Data saved to {csv_file_path}")
