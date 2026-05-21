# controllers/result_controller.py

from models.marks import MarksModel
from models.result import ResultModel


class ResultController:

    @staticmethod
    def processing_pipeline(student_id):

        marks = MarksModel.get_marks(student_id)

        if not marks:
            return False, "Marks not found."

        total = (
            marks['Maths'] +
            marks['DBMS'] +
            marks['Python'] +
            marks['OS'] +
            marks['Java']
        )

        percentage = total / 5.0

        # Grade logic
        if percentage >= 90:
            grade = "A+"

        elif percentage >= 75:
            grade = "A"

        elif percentage >= 60:
            grade = "B"

        elif percentage >= 40:
            grade = "C"

        else:
            grade = "F"

        status = "Pass" if percentage >= 40 else "Fail"

        ResultModel.save_result(
            student_id,
            total,
            percentage,
            grade,
            status
        )

        return True