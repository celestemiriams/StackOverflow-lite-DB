"""
Module for utilities
"""
import json
import re
from datetime import datetime


class Utils:
    """
    Class for date, time and Identifiers
    """

    @staticmethod
    def make_date_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def __create_unique_number():
        return datetime.now().strftime("%Y%m%d%H%M%S%f")

    @staticmethod
    def generate_question_id():
        return "QTN" + Utils.__create_unique_number()

    @staticmethod
    def generate_answer_id():
        return "ANS" + Utils.__create_unique_number()

    @staticmethod
    def generate_user_id():
        return "USR" + Utils.__create_unique_number()


class JSONSerializable(object):
    """
    Class with methods for JSON objects
    """

    def to_json(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.to_json()