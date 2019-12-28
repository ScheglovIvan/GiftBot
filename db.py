import psycopg2


class DataBase():
    def __init__(self):
        self.con = psycopg2.connect(
            host = "127.0.0.1",
            port = '5432',
            database = "gift_db",
            user = "postgres",
            password = "33546132"
        )
        self.cur = self.con.cursor()  


    def __del__(self):
        self.con.commit()  
        self.con.close()

    def newOrder(self, user_id, user_name, shop_name, price):
        self.cur.execute(
                "INSERT INTO orders (user_id, user_name, shop_name, price) VALUES (%d, %r, %r, %d)" % (user_id, user_name, shop_name, price)
            )

    def newLink(self, user_id, link):
        self.cur.execute("SELECT * FROM link WHERE link = %r" % (link))
        link_db = self.cur.fetchall()
        if not link_db:
            self.cur.execute(
                    "INSERT INTO link (user_id, link) VALUES (%d, %r)" % (user_id, link)
                )

    def getLink(self, user_id):
        self.cur.execute("SELECT * FROM link WHERE user_id = %d AND used = false ORDER BY id DESC LIMIT 1" % (user_id))
        link = self.cur.fetchall()
        if not link:
            pass
        else:
            self.cur.execute(
                "UPDATE link SET used = true WHERE link = %r" % (link[0][2])
                )
        return link


    def userBan(self, user_id):
        self.cur.execute("SELECT * FROM orders WHERE user_id = %d" % (user_id))
        user = self.cur.fetchall()

        if not user:
            return True
        else:
            return False

    def getOrder(self):
        self.cur.execute("SELECT * FROM orders")
        orders = self.cur.fetchall()
        return orders
