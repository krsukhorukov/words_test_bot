from imports import *

class Database:
    def __init__(self):
        # Старые атрибуты
        self.dbname = POSTGRES_DB
        self.user = POSTGRES_USER
        self.password = POSTGRES_PASSWORD
        self.host = POSTGRES_HOST
        self.port = POSTGRES_PORT
        
        self.engine = create_engine(
            f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        )

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
            select_query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(select_query, self.engine)
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

    def check_and_create_user(self, user_id, user_fullname, username):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM utilisateurs WHERE user_id = %s", (user_id,))
            user_exists = cursor.fetchone()

            if not user_exists:
                # Пользователя нет, вставляем новую запись
                cursor.execute(
                    "INSERT INTO utilisateurs (user_id, user_fullname, username) VALUES (%s, %s, %s)",
                    (user_id, user_fullname, username)
                )
                conn.commit()
                logger.success(f"Utilisateur id={user_id} créé avec succès.")
            else:
                # Пользователь уже существует, обновляем нужные поля
                cursor.execute(
                    "UPDATE utilisateurs SET user_fullname = %s, username = %s WHERE user_id = %s",
                    (user_fullname, username, user_id)
                )
                conn.commit()
                logger.success(f"Utilisateur id={user_id} mis à jour avec succès.")

        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            cursor.close()
            conn.close()


    def get_user_data(self, user_id, block_status=False):
        try:
            conn = self.get_connection()
            select_query = f"SELECT status_blocked, admin_status, commentaire FROM utilisateurs WHERE user_id = {user_id};"
            df = pd.read_sql_query(select_query, self.engine)
            select_query2 = f"SELECT only_admins FROM administration;"
            df2 = pd.read_sql_query(select_query2, self.engine)
            conn.close()

            status_blocked = df.loc[0, 'status_blocked']
            admin_status = df.loc[0, 'admin_status']
            commentaire = df.loc[0, 'commentaire']
            if commentaire == None:
                commentaire = "-"
            only_admins = df2.loc[0, 'only_admins']
            if block_status:
                return admin_status
            else:
                return status_blocked, admin_status, commentaire, only_admins

        except Exception as e:
            logger.error(f"Ошибка при извлечении данных: {e}")

    def get_users_table(self, is_keyboard=True):
        conn = self.get_connection()
        if is_keyboard:
            select_query = "SELECT * FROM utilisateurs"
            df_id = pd.read_sql_query(select_query, self.engine)
            result = df_id['user_id'].tolist()
        else:
            select_query = "SELECT number, user_id, user_fullname, username, admin_status FROM utilisateurs"
            df = pd.read_sql_query(select_query, self.engine)
            result = df.to_dict('records')
        
        conn.close()
        
        return result

    def change_admin_status(self, user_id, new_status):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("UPDATE utilisateurs SET admin_status = (%s) WHERE user_id = (%s);", (new_status, user_id))
            conn.commit()
            print("Статус успешно изменен")

        except:
            print("неа")
        finally:
            conn.close()

    def admin_mode(self, user_id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT only_admins FROM administration;")
            row = cursor.fetchone()

            if not row:
                print("В таблице нет записей!")
                return None

            only_admins = row[0]
        
            if only_admins is None:
                only_admins = False

            new_value = not only_admins

            cursor.execute("""
                UPDATE administration 
                SET only_admins = %s,
                    changed_by  = %s,
                    time        = NOW()
            """, (new_value, user_id))

            conn.commit()

            return new_value

        except Exception as e:
            print("Ошибка:", e)
            return None
        finally:
            conn.close()
