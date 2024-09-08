from enum import StrEnum
from sqlite3 import connect

from settings import get_settings, get_logger


settings = get_settings()
logger = get_logger(__name__)
connection = connect(settings.DB_PATH)
cursor = connection.cursor()



class DatabaseTables(StrEnum):
    USERS = "users"



class Storage:
    """This class defines functions for storing and retrieving user data"""
    data_cache = {}
    column_names: dict = {}


    @classmethod
    def setup_storage(cls):
        sql = f"""CREATE TABLE IF NOT EXISTS {DatabaseTables.USERS} (user_id INTEGER PRIMARY KEY, query_pair TEXT, query_search TEXT)"""
        cursor.execute(sql)
        connection.commit()

        # Generate tuple of column names for each table, used for setting their values in the cache
        cls.column_names = { table.value: tuple(i[1] for i in cursor.execute(f"""PRAGMA table_info({table.value})""").fetchall()) for table in DatabaseTables }



    @classmethod
    def setup_user_data(cls, user_id: int):
        """Setup user data in database and cache"""
        sql = f"""INSERT OR IGNORE INTO {DatabaseTables.USERS} (user_id) VALUES (?)"""
        cursor.execute(sql, (user_id,))
        connection.commit()

        user_data = {}
        for table in DatabaseTables:
            tablename = table.value

            # Insert an entry for the user in the table
            user_data[tablename] = {}
            sql = f"""INSERT OR IGNORE INTO {tablename} (user_id) VALUES (?)"""
            
            cursor.execute(sql, (user_id,))
            connection.commit()
            
            # Iterate over the column name and column value and set them in the cache, ignoring the user_id which is indexed at 0
            for key, value in zip(cls.column_names[tablename][1:], cursor.execute(f"""SELECT * FROM {tablename} WHERE user_id=?""", (user_id,)).fetchone()[1:] ):
                user_data[tablename][key] = value


        cls.data_cache[user_id] = user_data



    @classmethod
    def get_user_data(cls, user_id: int, tablename: str) -> dict:
        """Setup user data if not in cache and get requested table from cache"""
        if user_id not in cls.data_cache:
            cls.setup_user_data(user_id)
        
        user_data = cls.data_cache[user_id]
        assert tablename in user_data, f"{tablename} not a valid user data table"
        
        table = user_data[tablename]
        return table


    @classmethod
    def set_user_data(cls, user_id: int, tablename: str, **changes) -> None:
        """Command to set column values using keyword arguments in the database and cache"""
        if user_id not in cls.data_cache:
            cls.setup_user_data(user_id)

        user_data = cls.data_cache[user_id]
        assert tablename in user_data, f"{tablename} not a valid user data table"

        changes_string =  ", ".join(f"""{key}={changes[key]}""" for key in changes)
        sql = f"""UPDATE {tablename} SET {changes_string} WHERE user_id=?"""

        cursor.execute(sql, (user_id,))
        connection.commit()

        for key in changes:
            user_data[tablename][key] = changes[key]
        
        cls.data_cache[user_id] = user_data



def get_storage() -> Storage:
    return Storage()


get_storage().setup_storage()

