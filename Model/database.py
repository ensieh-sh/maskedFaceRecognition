import os.path

from Database import sqlite

class DatabaseModel:
    def __init__(self):
        db_file_found = self.database_file_found()

        self.conn = sqlite.connect_to_db()

        if not db_file_found:
            self.create_database_tables()

    @staticmethod
    def database_file_found():
        return os.path.isfile('./covid.db')

    def create_database_tables(self):
        sqlite.create_all_tables(self.conn)


    def insert_attendance(self, name, time, mask, state):
        sqlite.insert_attendance(self.conn, name, time, mask, state)



    def select_last_login_by_name(self, name):
        row = sqlite.select_last_login_by_name(self.conn, name)
        user = self.user_row_to_user_dict(row)
        return user


    def select_all_by_name(self, name):
        rows = sqlite.select_all_by_name(self.conn, name)
        return rows

    def select_all_date(self,date):
        rows = sqlite.select_all_by_date(self.conn, date)
        return rows


    @staticmethod
    def user_row_to_user_dict(row):
        if row is not None:
            user = {
                'name': row[0],
                'time': row[1],
                'mask': row[2],
                'state': row[3],

            }
            return user
        else:
            return None



