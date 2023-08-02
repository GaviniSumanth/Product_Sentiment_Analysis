import sqlite3
import warnings
import os
import dill as pickle
from datetime import datetime
import json

TABLES = """
    CREATE TABLE MODELS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CREATED_AT DATETIME  NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
        UPDATED_AT DATETIME  NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
        NAME TEXT UNIQUE NOT NULL,
        DESCRIPTION TEXT NOT NULL,
        MODEL BLOB NOT NULL,
        INPUT_FIELDS TEXT NOT NULL
    );
"""


def get_db():
    package_dir = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(package_dir, "db")):
        os.mkdir(os.path.join(package_dir, "db"))

    db_path = os.path.join(package_dir, "db/models.sqlite")
    db_found = os.path.isfile(db_path)
    if not db_found:
        try:
            warnings.warn("DB_NOT_FOUND: Creating a new models database")
            conn = sqlite3.connect(db_path)
            conn.execute(TABLES)
        except Exception as e:
            print("DB_CREATION_FAILED:", e)
        finally:
            conn.close()

    return db_path


class Storage:
    def __init__(self):
        self.db_path = get_db()

    def add_model(self, name, description, model, input_fields):
        data = (name, description, pickle.dumps(model), json.dumps(input_fields))
        add_model_query = """ 
            INSERT INTO MODELS
            (NAME, DESCRIPTION, MODEL, INPUT_FIELDS)
            VALUES (?, ?, ?, ?);
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(add_model_query, data)
            conn.commit()
        except sqlite3.Error as error:
            print("INSERTION_FAILED:", error)

    def update_model(self, name, model):
        data = (pickle.dumps(model), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name)
        update_model_query = """
            UPDATE MODELS SET MODEL = ?, UPDATED_AT=? WHERE NAME = ?;
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(update_model_query, data).fetchone()
            conn.commit()
        except sqlite3.Error as error:
            print("UPDATE_FAILED:", error)

    def delete_model(self, name):
        data = tuple([name])
        delete_model_query = """
            DELETE FROM MODELS WHERE NAME = ?;
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(delete_model_query, data).fetchone()
            conn.commit()
        except sqlite3.Error as error:
            print("DELETION_FAILED:", error)

    def get_model(self, name):
        data = tuple([name])
        get_model_query = """
            SELECT MODEL FROM MODELS WHERE NAME = ?;
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            row = cursor.execute(get_model_query, data).fetchone()
        except sqlite3.Error as error:
            print("RETRIEVAL_FAILED:", error)
        return pickle.loads(row["model"])


class Info:
    def __init__(self):
        self.db_path = get_db()

    def get_info(self, offset):
        data = tuple([str(offset)])
        get_info_query = """
            SELECT NAME, DESCRIPTION FROM MODELS LIMIT 10 OFFSET ?;
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute(get_info_query, data).fetchall()
        except sqlite3.Error as error:
            print("Exception:", error)
            raise error
        data = []
        for i in rows:
            data.append({"name": i["name"], "description": i["description"]})
        return data

    def get_fields(self, name):
        data = tuple([name])
        get_model_query = """
            SELECT INPUT_FIELDS FROM MODELS WHERE NAME = ?;
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            row = cursor.execute(get_model_query, data).fetchone()
        except sqlite3.Error as error:
            print("RETRIEVAL_FAILED:", error)
        if row:
            return row["input_fields"]


class Wrapper:
    def __init__(self, model, *args, **kwargs) -> None:
        self.model = model
        self.args = args
        self.kwargs = kwargs

    def predict(self, *args, **kwargs):
        raise NotImplementedError
