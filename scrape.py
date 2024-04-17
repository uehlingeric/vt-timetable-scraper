import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


class TimetableScraper:
    BASE_URL = 'https://apps.es.vt.edu/ssb/HZSKVTSC.P_ProcRequest'
    DATA_KEYS = [
        'crn', 'course', 'title', 'schedule_type', 'modality', 'cr_hrs',
        'capacity', 'instructor', 'days', 'start_time', 'end_time',
        'location', 'exam'
    ]

    def __init__(self, driver):
        """
        Initialize the scraper with a Selenium WebDriver.
        :param driver: A Selenium WebDriver instance to interact with the browser.
        """
        self.driver = driver

    def fetch_courses(self, term_year, subject_codes):
        """
        Fetches course data for a given term and list of subject codes.
        :param term_year: The term year as a string (e.g., '202401' for Spring 2024).
        :param subject_codes: A list of subject codes to fetch data for.
        :return: A list of dictionaries containing course data.
        """
        self._navigate_to_page(term_year)
        all_courses = []
        for code in subject_codes:
            all_courses.extend(self._fetch_subject_data(code))
        return all_courses

    def _navigate_to_page(self, term_year):
        """
        Navigates to the timetable page and selects the given term.
        :param term_year: The term year to select on the webpage.
        """
        self.driver.get(self.BASE_URL)
        time.sleep(2)  # Wait for page to load
        Select(self.driver.find_element(By.NAME, 'TERMYEAR')
               ).select_by_value(term_year)
        time.sleep(2)

    def _fetch_subject_data(self, subject_code):
        """
        Selects a subject from the dropdown and fetches course data for it.
        :param subject_code: The subject code to select.
        :return: A list of course data dictionaries for the selected subject.
        """
        Select(self.driver.find_element(By.NAME, 'subj_code')
               ).select_by_value(subject_code)
        self.driver.find_element(By.NAME, "BTN_PRESSED").click()
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return self._parse_table(soup)

    def _parse_table(self, soup):
        """
        Parses the HTML table of courses from the page source.
        :param soup: BeautifulSoup object containing the page HTML.
        :return: A list of course data dictionaries.
        """
        table = soup.find('table', attrs={'class': 'dataentrytable'})
        if not table:
            return []
        rows = [row for row in table.find_all('tr') if row.attrs == {}]
        return [self._parse_row(row) for row in rows if row.find_all('td')]

    def _parse_row(self, row):
        """
        Parses a single row of the course table.
        :param row: A BeautifulSoup Tag object representing a table row.
        :return: A dictionary with course data extracted from the row.
        """
        entries = [td.text.strip().replace('\n', ' ')
                   for td in row.find_all('td')]
        return dict(zip(self.DATA_KEYS, entries))


def save_to_csv(data, filename):
    pd.DataFrame(data).to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def main():
    term_year = '202409'  # Edit for specific term: Ex - 202409 = Fall 2024, year_month format

    subject_codes = [
        'AAD', 'AAEC', 'ACIS', 'ADV', 'AFST', 'AHRM', 'AINS', 'AIS', 'ALCE', 'ALS',
        'AOE', 'APS', 'APSC', 'ARBC', 'ARCH', 'ART', 'AS', 'ASPT', 'AT', 'BC',
        'BCHM', 'BDS', 'BIOL', 'BIT', 'BMES', 'BMSP', 'BMVS', 'BSE', 'CEE',
        'CEM', 'CHE', 'CHEM', 'CHN', 'CINE', 'CLA', 'CMDA', 'CMST', 'CNST', 'COMM',
        'CONS', 'COS', 'CRIM', 'CS', 'CSES', 'DANC', 'DASC', 'ECE', 'ECON', 'EDCI',
        'EDCO', 'EDCT', 'EDEL', 'EDEP', 'EDHE', 'EDIT', 'EDP', 'EDRE', 'EDTE', 'ENGE',
        'ENGL', 'ENGR', 'ENSC', 'ENT', 'ESM', 'FIN', 'FIW', 'FL', 'FMD', 'FR',
        'FREC', 'FST', 'GBCB', 'GEOG', 'GEOS', 'GER', 'GIA', 'GR', 'GRAD', 'HD',
        'HEB', 'HIST', 'HNFE', 'HORT', 'HTM', 'HUM', 'IDS', 'IS', 'ISC', 'ISE',
        'ITAL', 'ITDS', 'JMC', 'JPN', 'JUD', 'LAHS', 'LAR', 'LAT', 'LDRS', 'MACR',
        'MATH', 'ME', 'MGT', 'MINE', 'MKTG', 'MN', 'MS', 'MSE', 'MTRG', 'MUS',
        'NANO', 'NEUR', 'NR', 'NSEG', 'PAPA', 'PHIL', 'PHS', 'PHYS', 'PM', 'PORT',
        'PPE', 'PPWS', 'PR', 'PSCI', 'PSVP', 'PSYC', 'REAL', 'RED', 'RLCL', 'RTM',
        'RUS', 'SBIO', 'SOC', 'SPAN', 'SPES', 'SPIA', 'STAT', 'STL', 'STS', 'SYSB',
        'TA', 'TBMH', 'UAP', 'UH', 'UNIV', 'VM', 'WATR', 'WGS'
    ]

    driver = webdriver.Chrome()

    try:
        scraper = TimetableScraper(driver)
        all_courses = scraper.fetch_courses(term_year, subject_codes)
        if all_courses:
            save_to_csv(all_courses, 'offered_raw.csv')
        else:
            print("No courses found.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
