"""
This module is responsible for answer end points.
"""
from flask import jsonify, request
from api.models.database_transaction import DbTransaction
from api.models.questions import QuestionsHandler
from api.models.error_messages import ErrorMessage


class AnswerModel(object):
    """
    This class contains methods that handle specific
    answers 
    """

    error_message = ErrorMessage()

    sql = """ """

    def return_all_answers(self, question_id=None, user_id=None):
        """
        This method returns all answers posted to a specific question
        """
        confirm_id = None
        answer_sql = None
        answer_data = None

        if question_id:
            confirm_id = DbTransaction.retrieve_one(
                """SELECT "question_id" FROM "question" WHERE "question_id" = %s""",
                (question_id, ))
            answer_sql = answer_sql = self.sql + """ WHERE "answer".question_id = %s"""
            answer_data = (question_id, )
        else:
            confirm_id = DbTransaction.retrieve_one(
                """SELECT "user_id" FROM "user" WHERE "user_id" = %s""",
                (user_id, ))
            answer_sql = self.sql + """ WHERE "answer".user_id = %s"""
            answer_data = (user_id, )

        if confirm_id:
            answers_turple_list = DbTransaction.retrieve_all(answer_sql, answer_data)
            answer_list = []
            for answer_tuple in answers_turple_list:
                answer_dict = {
                    "answer": answer_tuple[0],
                    "answer_id": answer_tuple[1],
                    "user_id": answer_tuple[2],
                    "question_id": answer_tuple[3]
                }
                answer_list.append(answer_dict)

            return jsonify({"message": "result retrieved successfully",
                            "answers": answer_list}), 200
        # if question_id:
        #     RidesHandler.no_user_found_response("No answers found", question_id)
        # return self.error_message.no_answer_available(ride_id)

