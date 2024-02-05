import psycopg2


class db_operations:

    def __init__(self) -> None:
        pass


    def establish_connection(self):
       conn = psycopg2.connect(database="projectdb", user="postgres", password="admin123", host="127.0.0.1",
                                port="5432")
       return conn
    
    def insert_data(self,username,email,password):
        conn = self.establish_connection()
        curr= conn.cursor()
        try:
            curr.execute(f"INSERT INTO users (username, email, password) VALUES ('{username}','{email}','{password}')")
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            conn.close()

    def email_exists(self,email):
        conn=self.establish_connection()
        curr = conn.cursor()
        curr.execute("Select * FROM users where email = %s", (email,))
        rows = curr.fetchall()
        if len(rows) >=1:
            #print("Account already registered with this account")
            return True
        else:
            return False
    
    def login_user(self,email, password):
        conn = self.establish_connection()
        curr = conn.cursor()
        curr.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        rows = curr.fetchall()
        count = len(rows)
        if count == 1:
            return True
        else:
            return False
    
    def get_name(self,email, password):
        username =''
        conn = self.establish_connection()
        curr = conn.cursor()
        curr.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        rows = curr.fetchall()
        count = len(rows)
        if count == 1:
            username = rows[0][1]
            return username
        return None
    
    def confirm_password(self,email):
        conn = self.establish_connection()
        curr = conn.cursor()
        if(self.email_exists(email)):
            curr.execute("Select * FROM users where email = %s", (email,))
            rows = curr.fetchall()
            count = len(rows)
            if count == 1:
                db_password = rows[0][3]
                return db_password
        return None
