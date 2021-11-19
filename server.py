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

    def delete_automobili(self):
        cursor = self.db.cursor()
        sql = """
            DROP TABLE automobili
        """
        cursor.execute(sql)
        self.db.commit()

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


def upisi_poruku(lb, poruka):
    global COUNT
    lb.insert(COUNT, poruka)
    COUNT += 1


def serve(lb):
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
            upisi_poruku(lb, """-------------------""")
            if data[0] == "kreiraj_tabelu":
                upisi_poruku(lb, "kreiraj_tabelu")
                db.create_automobili()
                res = "tabela_dodata\n"
                conn.send(res.encode())
                upisi_poruku(lb, res)

            if data[0] == "obrisi_tabelu":
                print("obrisi tabelu")
                db.delete_automobili()
                print("obrisano")

            if data[0] == "dodaj_zapis":
                # lb.insert(END, "\n")
                upisi_poruku(lb, "dodaj_zapis")
                db.insert(data[1], data[2])
                res = """zapis_dodat:\nnaziv: {}\ncena: {}\n""".format(data[1], data[2])
                conn.send(res.encode())
                for message in res.split("\n"):
                    upisi_poruku(lb, message)

            if data[0] == "obrisi_zapis":
                upisi_poruku(lb, "obrisi_zapis")
                db.remove(data[1])
                res = """zapis_obrisan:\nID: {}\n""".format(data[1])
                conn.send(res.encode())
                for message in res.split("\n"):
                    upisi_poruku(lb, message)

            if data[0] == "nadji_zapis_id":
                # lb.insert(END, "\n")
                upisi_poruku(lb, "nadji_zapis_id")
                zapis = db.find_by_id(data[1])
                if zapis is None:
                    res = """nije_pronadjen:\nID: {}\n""".format(data[1])
                else:
                    response = """zapis_nadjen:"""
                    res = list(zapis)
                    messages = response.split("\n") + res
                    # lista = list()
                    # str1 = """a\nb\n"""
                    # strl = str1.split("\n")
                    # lista += strl
                    # lista.insert(2, "1")
                    # for i in lista:
                    #     print(i)
                    for message in messages:
                        upisi_poruku(lb, message)
                    res.insert(0, response)
                conn.send(str(res).encode())
                # lb.insert(END, res + "\n")
                # upisi_poruku(lb, res)

            if data[0] == "nadji_po_nazivu":
                # lb.insert(END, "nadji_po_nazivu\n")
                upisi_poruku(lb, "nadji_po_nazivu")
                zapis = db.find_by_naziv(data[1])
                if zapis is None:
                    res = """nije_pronadjen:\nnaziv: {}\n""".format(data[2])
                else:
                    res = list(zapis)
                    response = """zapis_najden:\nnaziv: {}\n""".format(zapis[1])
                    messages = response.split("\n") + res
                    # lista = list()
                    # str1 = """a\nb\n"""
                    # strl = str1.split("\n")
                    # lista += strl
                    # lista.insert(2, "1")
                    # for i in lista:
                    #     print(i)
                    for message in messages:
                        upisi_poruku(lb, message)
                    res.insert(0, response)
                conn.send(str(res).encode())
                # lb.insert(END, res + "\n")
                # upisi_poruku(lb, res)

            if data[0] == "update_naziv":
                # lb.insert(END, "update_naziv\n")
                upisi_poruku(lb, "update_naziv")
                db.update(data[1], data[2])
                res = """zapis_update:\nID: {}\nnaziv: {}""".format(data[1], data[2])
                conn.send(res.encode())
                # lb.insert(END, res + "\n")
                # messages = response.split("\n") + res
                # lista = list()
                # str1 = """a\nb\n"""
                # strl = str1.split("\n")
                # lista += strl
                # lista.insert(2, "1")
                # for i in lista:
                #     print(i)
                for message in res.split("\n"):
                    upisi_poruku(lb, message)
                # res.insert(0, response)
                # upisi_poruku(lb, res)

        else:
            break


def interface():
    root = Tk()
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(100, 800))
    lb = Listbox(root, height=800)
    lb.pack()
    Thread(target=lambda: serve(lb), daemon=False).start()
    root.mainloop()


interface()
