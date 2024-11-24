# Import necessary libraries
import os
import matplotlib.pyplot as plt

# File paths
DATA_DIR = "data/"
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, "assignments.txt")
SUBMISSIONS_DIR = os.path.join(DATA_DIR, "submissions")

# Helper functions to read files
def read_students():
    students = {}
    with open(STUDENTS_FILE, 'r') as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 2:
                name, student_id = parts
                students[name.strip().lower()] = student_id.strip()
    return students

def read_assignments():
    assignments = {}
    with open(ASSIGNMENTS_FILE, 'r') as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 3:
                name, assignment_id, points = parts
                assignments[name.strip().lower()] = (assignment_id.strip(), int(points.strip()))
    return assignments

def read_submissions():
    submissions = []
    for submission_file in os.listdir(SUBMISSIONS_DIR):
        file_path = os.path.join(SUBMISSIONS_DIR, submission_file)
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    student_id, assignment_id, percentage = parts
                    submissions.append((student_id.strip(), assignment_id.strip(), float(percentage.strip())))
    return submissions

# Option 1: Calculate student's total grade
def calculate_student_grade(student_name, students, assignments, submissions):
    # Normalize the student name for case-insensitive comparison
    normalized_name = student_name.strip().lower()
    student_id = students.get(normalized_name)

    if not student_id:
        print("Student not found")
        return

    total_points = 0
    earned_points = 0

    for submission in submissions:
        if submission[0] == student_id:
            assignment_id = submission[1]
            percentage = submission[2]

            # Find assignment total points
            for name, (a_id, points) in assignments.items():
                if a_id == assignment_id:
                    earned_points += points * (percentage / 100)
                    total_points += points
                    break

    grade_percentage = (earned_points / total_points) * 100 if total_points > 0 else 0
    print(f"{round(grade_percentage)}%")

# Option 2: Assignment statistics
def assignment_statistics(assignment_name, assignments, submissions):
    # Normalize the assignment name for case-insensitive comparison
    normalized_name = assignment_name.strip().lower()
    match = assignments.get(normalized_name)

    if not match:
        print("Assignment not found")
        return

    assignment_id, _ = match
    scores = [submission[2] for submission in submissions if submission[1] == assignment_id]

    if not scores:
        print("No scores found for the assignment.")
        return

    print(f"Min: {min(scores):.0f}%")
    print(f"Avg: {sum(scores) / len(scores):.0f}%")
    print(f"Max: {max(scores):.0f}%")

# Option 3: Generate histogram
def generate_histogram(assignment_name, assignments, submissions):
    # Normalize input for case-insensitive comparison
    normalized_name = assignment_name.strip().lower()
    match = assignments.get(normalized_name)

    if not match:
        print("Assignment not found")
        return

    assignment_id, _ = match
    scores = [submission[2] for submission in submissions if submission[1] == assignment_id]

    if not scores:
        print("No scores found for the assignment.")
        return

    # Plot histogram
    plt.hist(scores, bins=[0, 25, 50, 75, 100], edgecolor="black")
    plt.title(f"Score Distribution for {assignment_name.title()}")
    plt.xlabel("Score Ranges (%)")
    plt.ylabel("Frequency")
    plt.show()

# Main program
def main():
    # Load data
    students = read_students()
    assignments = read_assignments()
    submissions = read_submissions()

    # Display menu
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph\n")

    choice = input("Enter your selection: ")

    if choice == "1":
        student_name = input("What is the student's name: ")
        calculate_student_grade(student_name, students, assignments, submissions)
    elif choice == "2":
        assignment_name = input("What is the assignment name: ")
        assignment_statistics(assignment_name, assignments, submissions)
    elif choice == "3":
        assignment_name = input("What is the assignment name: ")
        generate_histogram(assignment_name, assignments, submissions)
    else:
        print("Invalid selection. Program exiting.")

if __name__ == "__main__":
    main()
