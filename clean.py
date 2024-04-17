import csv

def standardize_modality(modality):
    """
    Standardizes the modality value from the raw data to a predefined set of short forms.
    This method maps longer modality descriptions to concise, standardized abbreviations.
    """
    return {
        'Face-to-Face Instruction': 'F2F',
        'Hybrid (F2F & Online Instruc.)': 'Hybrid',
        'Online with Synchronous Mtgs.': 'OnlineSync',
        'Online: Asynchronous': 'OnlineAsync',
        '': 'F2F'
    }.get(modality, modality)

def get_department(course):
    """
    Extracts the department code from the course value.
    This is typically the first part of the course string.
    """
    return course.split('-')[0]

def process_csv(input_filename, output_filename):
    """
    Processes the raw CSV file and outputs a cleaned and standardized version.
    This method reads course data, standardizes and enriches it with modality abbreviations, 
    and corrects any inconsistencies in time and location data.
    """
    with open(input_filename, 'r') as infile, open(output_filename, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['crn', 'dept', 'course_id', 'instructor', 'title', 'modality',
                      'credits', 'capacity', 'days', 'start_time', 'end_time', 'location']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            try:
                credits = int(row['cr_hrs'])
                if credits == 0:
                    continue
            except ValueError:
                continue

            modality_standardized = standardize_modality(row['modality'])
            department = get_department(row['course'])
            course_id = row['course'].replace('-', ' ')

            if row['days'] == '(ARR)':  # Handle '(ARR)' in Days
                row['start_time'], row['end_time'] = '(ARR)', '(ARR)'

            new_row = {
                'crn': row['crn'],
                'dept': department,
                'course_id': course_id,
                'instructor': row['instructor'],
                'title': row['title'],
                'modality': modality_standardized,
                'credits': row['cr_hrs'],
                'capacity': row['capacity'],
                'days': row['days'],
                'start_time': row['start_time'],
                'end_time': row['end_time'],
                'location': row['location']
            }

            writer.writerow(new_row)

def main():
    process_csv('offered_raw.csv', 'cleaned_offered.csv')

if __name__ == "__main__":
    main()
