# Crawler for STJ - Supremo tribunal de justiça

This bot was made to scrape judgment data from the source STJ. It didn't create the logic for checking if there is next page or if there is data, because the main purpose of this project was to remember the selenium basics.

# Flow

1. Enter in the source
2. Click in a button to show the search form
3. Fill the form
4. Search
5. Get the documents
6. Save the documents in a jsonl file
8. Click on the next page button
9. Repeat from 5th to 8th step until something break the code