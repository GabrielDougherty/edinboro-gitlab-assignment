#!/usr/bin/env python3
import csv

# parse student csv file for students taking specified course
def parse_students(file_name, course_number, class_section):
    students = []
    # --file-name flag not set
    if(file_name is None):
        print("File could not be found. Make sure you have used the '--file-name' flag correctly.")
        sys.exit()
    else:
        # Try to open the file for reading
        try: 
            file = open(file_name, 'r', newline='')
        except FileNotFoundError:
            print("File could not be found. Make sure file exists in this directory, and you have typed the name correctly.")
            sys.exit()

    studentreader = csv.reader(file, delimiter=',')
    # Search file for students    
    for line in studentreader:
        if (course_number == line[1] and class_section == line[2]):
            students.append(line)

    file.close()
    return students
