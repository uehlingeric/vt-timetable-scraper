# VTTimetableScraper

## Overview
VTTimetableScraper is a Python-based tool designed to extract course timetable information from Virginia Tech's timetable portal. The scraper navigates through the site, selects specific term years and subject codes, and captures detailed course information, which is then saved into a CSV file for further analysis or integration with other systems.

## Objective
The primary objective of VTTimetableScraper is to automate the collection of course data to facilitate academic planning, scheduling, and data analysis tasks. This tool helps users avoid manual data entry, reducing errors and saving time.

## Features
- **Automated Web Navigation**: Uses Selenium to interact with the university's timetable webpage.
- **Data Parsing**: Employs BeautifulSoup to extract and parse course data from HTML.
- **Data Extraction**: Extracts a comprehensive set of course details including CRN, course numbers, titles, modalities, credits, capacities, instructors, and more.
- **Output in CSV Format**: Saves the scraped data in a user-friendly CSV format, allowing easy integration with data analysis tools and spreadsheets.

## How It Works
The scraper performs the following steps:
1. Initializes a Selenium WebDriver to handle web interactions.
2. Navigates to the Virginia Tech timetable selection page.
3. Sequentially selects each subject code provided and scrapes available course data for the specified term year.
4. Parses the HTML content to extract detailed course information.
5. Saves the extracted data into a CSV file.

## Prerequisites
- Python 3.6 or higher
- Selenium
- BeautifulSoup4
- Pandas
- Webdriver for Chrome or Firefox (depending on your browser preference)

## Setup and Installation
1. **Install Python Dependencies**:
   ```bash
   pip install selenium beautifulsoup4 pandas
   ```
2. **Webdriver**:
 - Download the appropriate WebDriver for your browser:
 - - ChromeDriver
 - - GeckoDriver for Firefox
 - Ensure the WebDriver binary is in your PATH.
3. **Clone the Repository**:
   ```bash
   git clone https://github.com/uehlingeric/VTTimetableScraper
   cd VTTimetableScraper
   ```
## Usage
To run the scraper:

1. Modify the term_year and subject_codes in the main function to match the term and subjects you are interested in.
2. Execute the script:
   ```bash
   python scrape.py
   ```
3. Check the output CSV file named offered_raw.csv for the scraped data.
4. If you wish the clean the raw data, a cleaning script is provided as well:
   ```bash
   python clean.py
   ```
5. Check the output CSV file named cleaned_offered.csv for the cleaned data.
