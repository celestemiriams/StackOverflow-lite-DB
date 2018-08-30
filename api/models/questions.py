"""
This module handles specific requests made
on the API end points
"""
from flask import jsonify, request
from api.models.question import Question
from api.models.answer import Answer
from api.models.database_transaction import DbTransaction
from api.models.error_messages import ErrorMessage


class QuestionsHandler(object):
    """
    This class contains methods that handle specific
    requests made on the API end point
    """

    error_message = ErrorMessage()

    def return_all_questions(self, sql_statement, data=None):
        """
        This method returns all questions asked
        """
        sql = sql_statement
        questions_turple_list = []
        if  data is not None:
            questions_turple_list = DbTransaction.retrieve_all(sql, data)
        else:
            questions_turple_list = DbTransaction.retrieve_all(sql)

        question_list = []
        for question_list in questions_turple_list:
            question_dict = {
                "question_id": question_list[0],
                "user_id": question_list[1],
                "title": question_list[2],
                "question": question_list[3],
            }
            question_list.append(question_dict)
        return jsonify({"message": "results retrieved successfully",
                        "questions": question_list})

    def return_single_question(self, question_id):
        """
        This method returns a single question
        """
        request_sql = """SELECT "user".username, question.* FROM "question" LEFT JOIN "user"\
         ON(question.user_id = "user".user_id) WHERE "question_id" = %s """
        question_turple = DbTransaction.retrieve_one(request_sql, (question_id, ))

        if question_turple is not None:
            user_name = question_turple[0]
            question_id = question_turple[1]
            user_id = question_turple[2]
            title = question_turple[3]
            question = question_turple[4]
            
            return jsonify({"Status code": 200, "question": {
                "user_name": user_name,
                "question_id": question_id,
                "user_id": user_id,
                "title": title,
                "question": question
            },
                            "message": "result retrieved successfully"})
        return self.error_message.no_question_available(question_id)

    def post_question(self, user_id):
        """
        This method saves a question
        """
        keys = ("title", "question")
        if not set(keys).issubset(set(request.json)):
            return self.error_message.request_missing_fields()

        request_condition = [
            request.json["title"].strip(),
            request.json["question"].strip()
            ]

        if not all(request_condition):
            return self.error_message.fields_missing_information(request.json)

        user = DbTransaction.retrieve_one(
            """SELECT "user_id" FROM "user" WHERE "user_id" = %s""",
            (user_id, ))

        title = request.json['title']
        question = request.json['question']

        question = Question(user, title, question)

        question.save_question()
        return jsonify({"status_code": 201, "question": question.get_question_information(),
                        "message": "Question added successfully"}), 201

    def post_answer_to_question(self, user_id, question_id, answer):
        """
        This method saves an answer to a question 
        """
        db_question_id = DbTransaction.retrieve_one(
            """SELECT "question_id" FROM "question" WHERE "question_id" = %s""",
            (question_id, ))

        if db_question_id is None:
            return self.error_message.no_question_available(question_id)

        question_answer = Answer(user_id, question_id, answer)

        check_request = question_answer.check_answer_existance()
        if check_request["status"] == "failure":
            return jsonify({"message": check_request["message"]}), 400
        
        question_answer.save_answer()

        return jsonify({"Status code": 201, 
                       "request": question_answer.return_answer_information(),
                        "message": "request sent successfully"}), 201