"""
This module provides responses to url requests.
"""
from flask import jsonify, request
from flask.views import MethodView
from api.models.questions import QuestionsHandler
from api.models.answers import AnswerModel
from api.models.user import User


class QuestionViews(MethodView):
    """
    This class contains methods that respond to various url end points.
    """

    questions_handler = QuestionsHandler()

    def get(self, question_id):
        """
        All questions posted are returned if no question ID is specified
        :param question_id: Question id
        :return:
        """
        token = request.headers.get('auth_token')
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        decoded = User.decode_token(request.headers.get('auth_token'))
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])

        if User.check_login_status(decoded["user_id"]):
            if not question_id:
                request_sql = """SELECT "user".username, question.* FROM "question" LEFT JOIN "user"\
                ON(question.user_id = "user".user_id) WHERE "question".user_id != %s"""
                sql_data = (decoded["user_id"], )
                return self.questions_handler.return_all_questions(request_sql, sql_data)
            return self.questions_handler.return_single_question(question_id)
        return jsonify({"message": "Please login"}), 401

    def post(self, question_id):
        """"
        Handles post requests
        saves a question
        :return:
        """
        token = request.headers.get('auth_token')
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        decoded = User.decode_token(request.headers.get('auth_token'))
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])
        if User.check_login_status(decoded["user_id"]):
            if question_id:
                return self.questions_handler.post_answer_to_question(decoded["user_id"], question_id)
            if not request or not request.json:
                return jsonify({"status_code": 400, "data": str(request.data),
                                "error_message": "content not JSON"}), 400
            return self.questions_handler.post_question(decoded["user_id"])
        return jsonify({"message": "Please login"}), 401


class AnswerView(MethodView):
    """
    This class handles url endpoints for requests.
    """
    answer_model = AnswerModel()

    def get(self, question_id):
        """
        This method gets all answers posted for a question
        """
        token = request.headers.get('auth_token')
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        decoded = User.decode_token(request.headers.get('auth_token'))
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])
        if User.check_login_status(decoded["user_id"]):
            return self.request_model.return_all_answers(question_id)
        return jsonify({"message": "Please login"}), 401
    def put(self, question_id, answer_id):
        """
        This method 
        :param question_id: Question Id
        :param answer_id: Answer Id
        :return:
        """
        token = request.headers.get('auth_token')
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        decoded = User.decode_token(request.headers.get('auth_token'))
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])
        if User.check_login_status(decoded["user_id"]):
            return self.answer_model.edit_answer(question_id, answer_id)
        return jsonify({"message": "Please login"}), 401


# class AnswersGiven(MethodView):
#     """
#     This class handles answers posted to a specific question
#     """
#     answer = AnswerModel()
#     def get(self):
#         """
#         This method gets all answers given to a specific question
#         """
#         token = request.headers.get('auth_token')
#         if not token:
#             return jsonify({"message": "Token is missing"}), 401
#         decoded = User.decode_token(request.headers.get('auth_token'))
#         if decoded["state"] == "Failure":
#             return User.decode_failure(decoded["error_message"])
#         if User.check_login_status(decoded["user_id"]):
#             answer_sql = """SELECT "user".username, answer.* FROM "answer" LEFT JOIN "queston"\
#             ON(answer.question_id = "question".question_id) WHERE "question".question_id = %s """
#             ##sql_data = (decoded["user_id"], )
#             return self.answers.return_all_answers(answer_sql, sql_data)
#             ##return self.answer.return_all_answers(decoded["user_id"])
#         return jsonify({"message": "Please login"}), 401


# class QuestionsAsked(MethodView):
#     """
#     This class handles questions posted
#     """
#     questions = QuestionsHandler()
#     answer = AnswerModel()
#     def get(self):
#         """
#         This method gets all questions posted by a specific user
#         """
#         token = request.headers.get('auth_token')
#         if not token:
#             return jsonify({"message": "Token is missing"}), 401
#         decoded = User.decode_token(request.headers.get('auth_token'))
#         if decoded["state"] == "Failure":
#             return User.decode_failure(decoded["error_message"])
#         if User.check_login_status(decoded["user_id"]):
#             question_sql = """SELECT "user".username, question.* FROM "question" LEFT JOIN "user"\
#             ON(question.user_id = "user".user_id) WHERE "user".user_id = %s """
#             sql_data = (decoded["user_id"], )
#             return self.questions.return_all_questions(question_sql, sql_data)
#         return jsonify({"message": "Please login"}), 401