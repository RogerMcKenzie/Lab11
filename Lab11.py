import os
import matplotlib.pyplot as plt

# File paths
DATA_DIR = "data/"
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, "assignments.txt")
SUBMISSIONS_DIR = os.path.join(DATA_DIR, "submissions")

def read_students():
    students = {}
    with open(STUDENTS_FILE, 'r') as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 2:
                student_id, name = parts
                students[name.strip()] = student_id.strip()
    return students

def read_assignments():
    assignments = {}
    with open(ASSIGNMENTS_FILE, 'r') as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 3:
                assignment_id, name, points = parts
                assignments[name.strip()] = (assignment_id.strip(), int(points.strip()))
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

def calculate_student_grade(student_name, students, assignments, submissions):
    if student_name not in students:
        print("Student not found")
        return
    
    student_id = students[student_name]
    total_points = 0
    earned_points = 0
    
    for submission in submissions:
        if submission[0] == student_id:
            assignment_id = submission[1]
            percentage = submission[2]
            for name, (a_id, points) in assignments.items():
                if a_id == assignment_id:
                    earned_points += points * (percentage / 100)
                    total_points += points
                    break
    
    if total_points > 0:
        grade_percentage = (earned_points / total_points) * 100
        print(f"{round(grade_percentage)}%")
        
    grade_percentage = (earned_points / total_points) * 100 if total_points > 0 else 0
    print(f"{round(grade_percentage)}%")

def assignment_statistics(assignment_name, assignments, submissions):
    if assignment_name not in assignments:
        print("Assignment not found")
        return
    
    assignment_id = assignments[assignment_name][0]
    scores = [submission[2] for submission in submissions if submission[1] == assignment_id]
    
    if scores:
        print(f"Min: {int(min(scores))}%")
        print(f"Avg: {int(sum(scores) / len(scores))}%")
        print(f"Max: {int(max(scores))}%")

def generate_histogram(assignment_name, assignments, submissions):
    if assignment_name not in assignments:
        print("Assignment not found")
        return
    
    assignment_id = assignments[assignment_name][0]
    scores = [submission[2] for submission in submissions if submission[1] == assignment_id]
    
    if scores:
        plt.hist(scores, bins=[0, 25, 50, 75, 100], edgecolor="black")
        plt.title(f"Score Distribution for {assignment_name}")
        plt.xlabel("Score Ranges (%)")
        plt.ylabel("Frequency")
        plt.show()

def main():
    students = read_students()
    assignments = read_assignments()
    submissions = read_submissions()

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    
    choice = input("Enter your selection: ").strip()
    
    if choice == "1":
        student_name = input("What is the student's name: ").strip()
        calculate_student_grade(student_name, students, assignments, submissions)
    elif choice == "2":
        assignment_name = input("What is the assignment name: ").strip()
        assignment_statistics(assignment_name, assignments, submissions)
    elif choice == "3":
        assignment_name = input("What is the assignment name: ").strip()
        generate_histogram(assignment_name, assignments, submissions)

if __name__ == "__main__":
    main()
