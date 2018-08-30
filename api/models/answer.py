"""
This module is an answer model with its attributes
"""
from api.models.database_transaction import DbTransaction


class Answer(object):
    """
    This class represents an answer entity
    """

    def __init__(self, user_id, question_id, answer,answer_id=None):
        self.user_id = user_id
        self.question_id = question_id
        self.answer = answer
        self.answer_id = answer_id

    def save_answer(self):
        """
        This method saves an answer to a question.
        """

        answer_sql = """INSERT INTO "answer"(user_id, question_id, answer)
            VALUES((%s), (%s), %s);"""
        answer_data = (self.user_id, self.question_id, self.answer)
        DbTransaction.save(answer_sql, answer_data)
        
    def return_answer_information(self):
        """
        This method returns answer details.
        """
        
        return {
            "user_id": self.user_id,
            "question_id": self.question_id,
            "answer": self.answer
        }
        
    def check_answer_existance(self):
        """
        Checks the existance of an answer to a question.
        """
        check_sql = """SELECT "user_id", "question_id" FROM "answer"
        WHERE "user_id" = %s AND "question_id" = %s"""
        answer_data = (self.user_id, self.question_id)
        question_answer = DbTransaction.retrieve_one(check_sql, answer_data)
        if question_answer is None:
            return {"status": "success", "message": "No answer to this question"}
        return answer_data