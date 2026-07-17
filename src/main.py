import json
import gspread

with open("config.json", "r") as f:
    config = json.load(f)

gc = gspread.service_account(filename="key.json")

sheet = gc.open_by_url(config["sheet_url"])



# Select a worksheet/tab
worksheet = sheet.worksheet("Test")

# Read data
data = worksheet.get_all_values()

print(data)