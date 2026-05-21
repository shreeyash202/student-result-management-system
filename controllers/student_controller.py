# controllers/student_controller.py
import csv
import io
from models.student import StudentModel

class StudentController:
    @staticmethod
    def register(student_id, name, course, semester, password):
        if not student_id.strip() or not name.strip():
            return False, "Required identification fields cannot be blank."
        
        success = StudentModel.create_student(student_id, name, course, semester, password)
        if success:
            return True, "Student identity record enrolled cleanly."
        return False, "Operation failed: Student Roll ID already exists."
    
    @staticmethod
    def remove(student_id):
        if not student_id:
            return False, "Invalid Student Identifier."
        
        from models.student import StudentModel
        StudentModel.delete_student(student_id)
        return True, f"Student {student_id} record deleted successfully."
    
    @staticmethod
    def bulk_upload(file_wrapper):
        if not file_wrapper or file_wrapper.filename == '':
            return False, "Validation Error: No file selected."
        
        if not file_wrapper.filename.endswith('.csv'):
            return False, "Validation Error: Please upload a valid .csv file."

        try:
            # Stream and decode the uploaded file bytes to text string lines
            stream = io.StringIO(file_wrapper.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)
            
            student_batch = []
            for row in csv_reader:
                # Basic validation cleanup
                s_id = row.get('student_id', '').strip()
                name = row.get('name', '').strip()
                course = row.get('course', '').strip()
                sem = row.get('semester', '').strip()
                pwd = row.get('password', '').strip()
                
                if s_id and name:
                    student_batch.append((s_id, name, course, sem, pwd))
            
            if not student_batch:
                return False, "Validation Error: The CSV file layout is empty or parsing failed."
                
            # Direct handoff to bulk data controller execution
            return StudentModel.bulk_insert_students(student_batch)
            
        except Exception as e:
            return False, f"System parsing failure: {str(e)}"