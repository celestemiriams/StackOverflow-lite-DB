"""
This module is a question model with its attributes
"""
from api.models.database_transaction import DbTransaction

class Question(object):
    """
    This class represents a Question entity
    """

    def __init__(self, *args):
        self.user_id = args[0]
        self.title = args[1]
        self.question = args[2]
        self.question_id = args[2]
    
    def save_question(self):
        """
        This method saves the question
        """

        question_sql = """INSERT INTO "question"(user_id, title, question)
        VALUES((%s), %s, %s);"""
        question_data = (
            self.user_id, self.title,
            self.question
            )
        DbTransaction.save(question_sql, question_data)

    def get_question_information(self):
        """
        This method returns the information of a question.
        """

        return {
            "title": self.title,
            "question": self.question
        }
