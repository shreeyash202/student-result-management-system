# controllers/marks_controller.py

import csv
import io

from models.marks import MarksModel
from controllers.result_controller import ResultController


class MarksController:

    @staticmethod
    def submit_marks(
        student_id,
        maths,
        dbms,
        python_marks,
        os_marks,
        java
    ):

        try:

            scores = [
                int(maths),
                int(dbms),
                int(python_marks),
                int(os_marks),
                int(java)
            ]

            # Validation
            if any(m < 0 or m > 100 for m in scores):
                return False, "Scores must be between 0 and 100."

            MarksModel.enter_marks(
                student_id,
                maths,
                dbms,
                python_marks,
                os_marks,
                java
            )

            ResultController.processing_pipeline(student_id)

            return True, "Marks submitted successfully."

        except ValueError:
            return False, "Marks must be numeric."

    @staticmethod
    def bulk_upload(file_wrapper):

        if not file_wrapper or file_wrapper.filename == '':
            return False, "No file selected."

        if not file_wrapper.filename.endswith('.csv'):
            return False, "Please upload a CSV file."

        try:

            stream = io.StringIO(
                file_wrapper.stream.read().decode("UTF8"),
                newline=None
            )

            csv_reader = csv.DictReader(stream)

            marks_batch = []

            for row in csv_reader:

                student_id = row['student_id']

                maths = int(row['maths'])
                dbms = int(row['dbms'])
                python_marks = int(row['python'])
                os_marks = int(row['os'])
                java = int(row['java'])

                marks_batch.append((
                    student_id,
                    maths,
                    dbms,
                    python_marks,
                    os_marks,
                    java
                ))

            success, message = MarksModel.bulk_insert_marks(marks_batch)

            # Auto result generation
            for mark in marks_batch:
                ResultController.processing_pipeline(mark[0])

            return success, message

        except Exception as e:
            return False, str(e)