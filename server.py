import socket
from tkinter import *
import pymysql
from threading import Thread

COUNT = 1

class DB:
    def __init__(self, host="localhost", port=3306, user="root", passwd="", db="baza01"):
        self.db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)

    def create_automobili(self):
        cursor = self.db.cursor()
        sql = """
            CREATE TABLE `automobili` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `naziv` VARCHAR(255),
                `cena` FLOAT,
                PRIMARY KEY (`id`)
            )
        """
        cursor.execute(sql)
        self.db.commit()

    def insert(self, naziv, cena):
        cursor = self.db.cursor()
        sql = """
            INSERT INTO `automobili`
            (`naziv`, `cena`) VALUES ('{}', '{}')
        """.format(naziv, cena)
        cursor.execute(sql)
        self.db.commit()

    def remove(self, id):
        cursor = self.db.cursor()
        sql = """
            DELETE FROM `automobili`
            WHERE id={}
        """.format(id)
        cursor.execute(sql)
        self.db.commit()

    def update(self, id, naziv):
        cursor = self.db.cursor()
        sql = """
            UPDATE `automobili` 
            SET naziv = '{}' 
            WHERE `id`={};
        """.format(naziv, id)
        cursor.execute(sql)
        self.db.commit()

    # def delete_automobili(self):
    #     cursor = self.db.cursor()
    #     sql = """
    #         DROP TABLE automobili
    #     """
    #     cursor.execute(sql)
    #     self.db.commit()

    def find_by_id(self, id):
        cursor = self.db.cursor()
        sql = """
            SELECT * FROM automobili
            WHERE id={}
        """.format(id)
        cursor.execute(sql)
        res = cursor.fetchone()
        return res

    def find_by_naziv(self, naziv):
        cursor = self.db.cursor()
        sql = """
            SELECT * FROM automobili
            WHERE `naziv` LIKE '%{}%'
        """.format(naziv)
        cursor.execute(sql)
        res = cursor.fetchone()
        return res


def serve(text):
    global COUNT
    db = DB()
    s = socket.socket()
    host = socket.gethostname()
    port = 13012
    s.bind((host, port))
    s.listen(5)
    print("Serving...")
    while True:
        conn, addr = s.accept()
        data = conn.recv(4098).decode('utf-8')
        data = eval(data)

        # print("data: " + str(data))
        if data:
            # conn.send("Uspesno primljena poruka".encode())

            if data[0] == "kreiraj_tabelu":
                text.insert(END, "kreiraj_tabelu\n")
                db.create_automobili()
                res = "tabela_dodata\n"
                conn.send(res.encode())
                text.insert(END, res + "\n")

            # if data[0] == "obrisi_tabelu":
            #     print("obrisi tabelu")
            #     db.delete_automobili()
            #     print("obrisano")

            if data[0] == "dodaj_zapis":
                text.insert(END, "dodaj_zapis\n")
                db.insert(data[1], data[2])
                res = """zapis_dodat:\nnaziv: {}\ncena: {}\n""".format(data[1], data[2])
                conn.send(res.encode())
                text.insert(END, res + "\n")

            if data[0] == "obrisi_zapis":
                text.insert(END, "obrisi_zapis\n")
                db.remove(data[1])
                res = """zapis_obrisan:\nID: {}\n""".format(data[1])
                conn.send(res.encode())
                text.insert(END, res + "\n")

            if data[0] == "nadji_zapis_id":
                text.insert(END, "nadji_zapis_id\n")
                zapis = list(db.find_by_id(data[1]))
                res = """zapis_najden:\nID: {}\n""".format(data[1])
                conn.send(str(zapis).encode())
                text.insert(END, res + "\n")

            if data[0] == "nadji_po_nazivu":
                text.insert(END, "nadji_po_nazivu\n")
                zapis = list(db.find_by_naziv(data[1]))
                res = """zapis_najden:\nID: {}\n""".format(data[1])
                conn.send(str(zapis).encode())
                text.insert(END, res + "\n")

            if data[0] == "update_naziv":
                text.insert(END, "nadji_po_nazivu\n")
                db.update(data[1], data[2])
                res = """zapis_update:\nID: {}\n""".format(data[1])
                conn.send(res.encode())
                text.insert(END, res + "\n")

        else:
            break


def interface():
    root = Tk()
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(100, 800))
    text = Text(root)
    text.pack()
    Thread(target=lambda: serve(text)).start()
    root.mainloop()


interface()
