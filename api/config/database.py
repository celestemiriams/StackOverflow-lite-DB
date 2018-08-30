"""
This module handles the database set up
"""
import os
import psycopg2

class DatabaseAccess(object):
    """
    This class contains methods to create a database connection
    """
    @staticmethod
    def database_connection():
        """
        This method creates a connection to the databse
        "dbname='stackoverflow' user='celestemiriams' host='localhost' password='lutwama@2' port='5432'"
        :retun: connection
        """

        connection = psycopg2.connect(
            "dbname='stackoverflow' user='celestemiriams' host='localhost' password='lutwama@2' port='5432'"
        )
        print("successfully connected")
        return connection

if __name__ == "__main__":
    DatabaseAccess.database_connection()
        

