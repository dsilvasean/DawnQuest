import re

url = "https://www.shaalaa.com/textbook-solutions/c/balbharati-solutions-history-and-civics-6th-standard-maharashtra-state-board-chapter-1.01-the-indian-subcontinent-and-history_3482"
db_name = "1.01 The Indian Subcontinent and History"
db_name = db_name.replace(" ", "-").lower()
print(db_name)
match = re.search(db_name, url)
print(match)
