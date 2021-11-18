import socket
from tkinter import *
import time
from threading import Thread

PORT = 13012
HOST = socket.gethostname()

COUNT = 1


def connect():
    s = socket.socket()
    try:
        s.connect((HOST, PORT))
        return s
    except:
        print("conn err")
        sys.exit()


def run_request_thread(callback):
    try:
        Thread(target=callback, args=()).start()
    except:
        print("conn err")


def interface():
    root = Tk()
    root.geometry('{}x{}'.format(800, 800))
    root.pack_propagate(0)

    # HEADER ----------------------------------

    header = Frame(root, width=800, height=50, highlightbackground="black", highlightthickness=1.)
    header.pack(expand=False)

    canvas = Canvas(header, bd=0, relief=SUNKEN, width=800, height=50)
    canvas.pack()

    def animate():
        images = []
        for i in range(8):
            image = PhotoImage(file="sprites/tile00" + str(i) + ".jpg")
            images.append(image)

        container = canvas.create_image(0, 0, anchor=NW, image=images[0])
        while True:
            for image in images:
                canvas.itemconfig(container, image=image)
                time.sleep(0.1)

    Thread(target=animate, args=()).start()

    # BODY -----------------------------------

    body = Frame(root, background='white', bd=1, width=800, height=700)
    body.grid_propagate(0)
    body.pack(side=TOP, expand=True)

    listbox_odgovori_servera = Listbox(body, width=132)

    # otvori tabelu
    def otb_click():
        global COUNT
        s = connect()
        s.send(str(["kreiraj_tabelu"]).encode())
        data = s.recv(1024)
        s.close()
        listbox_odgovori_servera.insert(COUNT, data)
        COUNT += 1

    otvori_tabelu_btn = Button(body, text="Napravi novu tabelu", command=lambda: run_request_thread(otb_click))
    otvori_tabelu_btn.grid(row=1, column=1)

    # # otvori tabelu
    # def mrs_click():
    #     s = connect()
    #     s.send(str(["obrisi_tabelu"]).encode())
    #     data = s.recv(1024)
    #     # print(data)
    #     s.close()
    #
    # obrisi_tabelu_btn = Button(body, text="Obrisi tabelu bre", command=lambda: run_request_thread(mrs_click))
    # obrisi_tabelu_btn.grid(row=1, column=2)

    label_naziv = Label(body, text="Naziv:", pady=10)
    label_naziv.grid(row=2, column=1)

    text_naziv = Text(body, height=1, width=40)
    text_naziv.grid(row=2, column=2)

    label_cena = Label(body, text="Cena:", pady=10)
    label_cena.grid(row=3, column=1)

    text_cena = Text(body, height=1, width=40)
    text_cena.grid(row=3, column=2)

    # dodaj zapis
    def dz_click():
        global COUNT
        s = connect()
        poruka = ["dodaj_zapis", text_naziv.get(1.0, END).strip(), text_cena.get(1.0, END).strip()]
        s.send(str(poruka).encode())
        data = s.recv(1024)
        s.close()
        listbox_odgovori_servera.insert(COUNT, data)
        COUNT += 1

    dodaj_zapis_btn = Button(body, text="Dodaj zapis", command=lambda: run_request_thread(dz_click))
    dodaj_zapis_btn.grid(row=4, column=2)

    label_nadji_id = Label(body, text="Naziv:", pady=10)
    label_nadji_id.grid(row=5, column=1)

    text_nadji_naziv = Text(body, height=1, width=40)
    text_nadji_naziv.grid(row=5, column=2)

    def nadji_po_nazivu():
        global COUNT
        s = connect()
        poruka = ["nadji_po_nazivu", text_nadji_naziv.get(1.0, END).strip()]
        s.send(str(poruka).encode())
        data = s.recv(1024)
        s.close()
        listbox_odgovori_servera.insert(COUNT, data)
        COUNT += 1
        parsed = eval(data)
        text_iscitan_naziv.delete(1.0, END)
        text_iscitan_naziv.insert(END, parsed[1])
        text_iscitan_id_prikaz.delete(1.0, END)
        text_iscitan_id_prikaz.insert(END, str(parsed[0]))

    obrisi_po_id_btn = Button(body, text="Nadji po nazivu", command=lambda: run_request_thread(nadji_po_nazivu))
    obrisi_po_id_btn.grid(row=5, column=3)

    label_citaj_po_id = Label(body, text="Nadji po ID:", pady=10)
    label_citaj_po_id.grid(row=6, column=1)

    text_nadji_id = Text(body, height=1, width=40)
    text_nadji_id.grid(row=6, column=2)

    def nadji_zapis_id_click():
        global COUNT
        global iscitan_id
        s = connect()
        poruka = ["nadji_zapis_id", text_nadji_id.get(1.0, END).strip()]
        s.send(str(poruka).encode())
        data = s.recv(1024)
        s.close()
        listbox_odgovori_servera.insert(COUNT, data)
        COUNT += 1
        parsed = eval(data)
        text_iscitan_naziv.delete(1.0, END)
        text_iscitan_naziv.insert(END, parsed[1])
        text_iscitan_id_prikaz.delete(1.0, END)
        text_iscitan_id_prikaz.insert(END, str(parsed[0]))

    nadji_po_id_btn = Button(body, text="Nadji po ID", command=lambda: run_request_thread(nadji_zapis_id_click))
    nadji_po_id_btn.grid(row=6, column=3)

    label_iscitan_id = Label(body, text="Iscitan ID:", pady=10)
    label_iscitan_id.grid(row=7, column=1)

    text_iscitan_id_prikaz = Text(body, height=1, width=40)
    text_iscitan_id_prikaz.grid(row=7, column=2)

    def obrisi_zapis_click():
        global COUNT
        s = connect()
        poruka = ["obrisi_zapis", text_iscitan_id_prikaz.get(1.0, END).strip()]
        s.send(str(poruka).encode())
        data = s.recv(1024)
        s.close()
        listbox_odgovori_servera.insert(COUNT, data)
        COUNT += 1

    obrisi_po_id_btn = Button(body, text="Obrisi po ID", command=lambda: run_request_thread(obrisi_zapis_click))
    obrisi_po_id_btn.grid(row=7, column=3)

    label_iscitan_naziv = Label(body, text="Iscitan naziv:", pady=10)
    label_iscitan_naziv.grid(row=8, column=1)

    text_iscitan_naziv = Text(body, height=1, width=40)
    text_iscitan_naziv.grid(row=8, column=2)

    def update_naziv():
        global COUNT
        s = connect()
        poruka = ["update_naziv", text_iscitan_id_prikaz.get(1.0, END).strip(), text_iscitan_naziv.get(1.0, END).strip()]
        s.send(str(poruka).encode())
        data = s.recv(1024)
        s.close()
        listbox_odgovori_servera.insert(COUNT, data)
        COUNT += 1

    obrisi_po_id_btn = Button(body, text="Update naziv", command=lambda: run_request_thread(update_naziv))
    obrisi_po_id_btn.grid(row=8, column=3)

    listbox_odgovori_servera.grid(row=10, column=1, columnspan=3, sticky='NSEW')

    # FOOTER ------------------------------

    footer = Frame(root, width=800, height=50, bd=1, highlightbackground="black", highlightthickness=1.)
    footer.pack_propagate(0)
    footer.pack(side=BOTTOM)

    footer_label = Label(footer, text="© 2021 Stefan Milicevic RIN-31/20 i Ljubisa Knezevic RIN-68/20")
    footer_label.pack(anchor=CENTER)

    root.mainloop()


interface()
