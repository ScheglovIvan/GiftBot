import psycopg2
from CONF import DB

class DataBase():
    def __init__(self):
        self.con = psycopg2.connect(
            host = DB['host'],
            port = DB['port'],
            database = DB['database'],
            user = DB['user'],
            password = DB['password']
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

    def getClick(self, *args):
        if not args:
            self.cur.execute("SELECT * FROM click")
            click = self.cur.fetchall()
        else:
            self.cur.execute("SELECT * FROM click ORDER BY id DESC LIMIT %d" % (args[0]))
            click = self.cur.fetchall()
        if not click:
            return False
        else:
            return click

    def getClickCount(self):
        self.cur.execute("SELECT id FROM click ORDER BY id DESC LIMIT 1")
        СlickCount = self.cur.fetchall()

        if not СlickCount:
            return False
        else:
            return СlickCount[0][0]
    
    
    def newClick(self, user_id, user_name):
        self.cur.execute("SELECT * FROM click WHERE user_id = %d" % (user_id))
        click = self.cur.fetchall()

        if not click:
            self.cur.execute(
                    "INSERT INTO click (user_id, user_name) VALUES (%d, %r)" % (user_id, user_name)
                )
        else:
            pass

    def ExitBan(self, user_id):
        self.cur.execute(
            "UPDATE orders SET user_id = 0 WHERE user_id = %d" % (user_id)
            )
        return "Бан отменен!!!"
