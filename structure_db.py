import psycopg2

def create_tables():
    commands = (
        """
        CREATE TABLE ORDERS (
            ID SERIAL PRIMARY KEY,
            USER_ID INT,
            USER_NAME CHAR(50),
            SHOP_NAME CHAR(50),
            PRICE INT
        )
        """,
        """
        CREATE TABLE LINK (
            ID SERIAL PRIMARY KEY,
            USER_ID INT,
            LINK CHAR(300),
            USED BOOLEAN DEFAULT FALSE
        )
        """,
        )

    con = psycopg2.connect(
        host = "127.0.0.1",
        port = '5432',
        database = "gift_db",
        user = "postgres",
        password = "33546132"
    )

    cur = con.cursor()

    for command in commands:
        cur.execute(command)

    print("Table created successfully")
    con.commit()  
    con.close()

if __name__ == '__main__':
    create_tables()