from imports import *

class VocabularyDatabase:
    def __init__(self):
        self.dbname = POSTGRES_DB
        self.user = POSTGRES_USER
        self.password = POSTGRES_PASSWORD
        self.host = POSTGRES_HOST
        self.port = POSTGRES_PORT

    def get_connection(self):
        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )


    def create_table(self, table_name):
        conn = self.get_connection()
        cursor = conn.cursor()

        create_table_query = sql.SQL("""
            CREATE TABLE {} (
                word TEXT PRIMARY KEY,
                translation TEXT
            )
        """).format(sql.Identifier(table_name))
        user_id = 123456

        try:
            cursor.execute(create_table_query)
            conn.commit()
            # Assuming there's another table named "vocabulary" where you want to insert metadata
            insert_query = sql.SQL('INSERT INTO vocabulary (name, user_id) VALUES (%s, %s)')
            cursor.execute(insert_query, (table_name, user_id))
            conn.commit()
            logger.info(f"Таблица '{table_name}' успешно создана.")
        except errors.DuplicateTable:
            logger.warning(f"Таблица '{table_name}' уже существует.")
        except Exception as e:
            logger.error(f"Ошибка при создании таблицы '{table_name}': {e}")
        finally:
            cursor.close()
            conn.close()

    def insert_words(self, table_name, words_dict):
        conn = self.get_connection()
        cursor = conn.cursor()

        insert_query = sql.SQL('INSERT INTO {} (word, translation) VALUES (%s, %s) ON CONFLICT (word) DO NOTHING').format(sql.Identifier(table_name))
        try:
            for word, translation in words_dict.items():
                cursor.execute(insert_query, (word, translation))
            conn.commit()
            logger.info(f"Слова успешно добавлены в таблицу '{table_name}'.")
        except Exception as e:
            logger.error(f"Ошибка при добавлении слов в таблицу '{table_name}': {e}")
        finally:
            cursor.close()
            conn.close()

    def db_get_words(self, table_name, is_dict=0):
        conn = self.get_connection()
        try:
            select_query = sql.SQL('SELECT * FROM {}').format(sql.Identifier(table_name))
            df = pd.read_sql_query(select_query.as_string(conn), conn)
            logger.info(f"Слова успешно извлечены из таблицы '{table_name}'.")
            if is_dict:
                word = df["word"]
                translation = df["translation"]
                return word.to_list(), translation.to_list()
            name = df["name"]
            return name.to_list()
        except Exception as e:
            logger.error(f"Ошибка при извлечении слов из таблицы '{table_name}': {e}")
            return pd.DataFrame(), pd.DataFrame()  # Return an empty DataFrame on error
        finally:
            conn.close()

    # def get_all_vocabulary(self):
    #     db_config = {
    #         'dbname': self.dbname,
    #         'user': self.user,
    #         'password': self.password,
    #         'host': self.host,
    #         'port': self.port
    #     }

    #     connection_string = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"

    #     engine = create_engine(connection_string)
    #     try:
    #         df = pd.read_sql_table("vocabulary", con=engine)
    #         logger.info("Словарь успешно извлечен из таблицы 'vocabulary'.")
    #         return df
    #     except Exception as e:
    #         logger.error(f"Ошибка при извлечении словаря из таблицы 'vocabulary': {e}")
    #         return pd.DataFrame()
