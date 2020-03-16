# -*- coding: cp1250 -*-
import sys, pickle, datetime
from PyQt4 import QtCore, QtGui, uic

klasa_formularza, klasa_bazowa = uic.loadUiType("wirtualnyZwierzak.ui")

class MojFormularz(klasa_bazowa, klasa_formularza):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.doktor = False
        self.wyprowadzanie = False
        self.sen = Flase
        self.jedzenie = False
        self.time_cycle = 0
        self.glod = 0
        self.szczescie = 8
        self.zdrowie = 8
        self.wymusObudzenie = False

        self.senRysunki = ["sleep1.gif", "sleep2.gif","sleep3.gif",
                           "sleep4.gif"]
        self.jedzenieRysunki = ["eat1.gif", "eat2.gif"]
        self.wyprowadzanieRysunki = ["walk1.gif", "walk2.gif", "walk3.gif",
                                     "walk4.gif"]
        self.zabawaRysunki = ["play1.gif", "play2.gif"]
        self.doktorRysunki = ["doc1.gif", "doc2.gif"]
        self.normalneRysunki = ["pet1.gif", "pet2.gif", "pet3.gif"]
        self.listaRysunkow = self.normalneRysunki
        self.rysunekIndeks = 0
        self.actionStop.triggered.connect(self.stop_klikniety)
        self.actionNakarm.triggered.connect(self.nakarm_klikniety)
        self.actionWyprowadz.triggered.connect(self.wyprowadz_klikniety)
        self.actionZabawa.triggered.connect(self.zabawa_klikniety)
        self.actionDoktor.triggered.connect(self.doktor_klikniety)
        self.mojTimer1 = QtCore.QTimer(self)
        self.mojTimer1.start(500)
        self.mojTimer1.timeout.connect(self.animacja_timer)
        self.mojTimer2 = QtCore.QTimer(self)
        self.mojTimer2.start(5000)
        self.mojTimer2.timeout.connect(self.tykniecie_timer)
        plikUchwyt = True
        try:
            plik = open("zapisane_dane_wz.pkl", "r")
        except:
            plikUchwyt = False
        if plikUchwyt:
            zapis_lista = pickle.load(plik)
            plik.close()
        else:
            zapis_lista = [8, 8, 0, datetime.datetime.now(), 0]

        self.szczescie = zapis_lista[0]
        self.zdrowie = zapis_lista[1]
        self.glod = zapis_lista[2]
        znacznik_czasu_wtedy = zapis_lista[3]
        self.cykl_zegara = zapis_lista[4]

        roznica = datetime.datetime.now() - znacznik_czasu_wtedy
        tykniecia = roznica.seconds / 50

        for i in range(0, tykniecia):
            self.cykl_zegara += 1
            if self.cykl_zegara == 60:
                self.cykl_zegara = 0
            if self.cykl_zegara <= 48:
                self.sen = False
                if self.glod < 8:
                    self.glod += 1

            else:
                self.sen = True
                if self.glod < 8 and self.cykl_zegara % 3 == 0:
                    self.glod += 1
            if self.glod == 7 and (self.cykl_egara % 2 == 0) \
               and self.zdrowie > 0:
                self.zdrowie -= 1
            if self.glod == 8 and self.zdrowie > 0:
                self.zdrowie -= 1

        if self.sen:
            self.listaRysunkow = self.senRysunki
        else:
            self.listaRysunkow = self.normalneRysunki

    def sprawdz_pobudka(self):
        if self.sen:
            wynik = (QtGui.QMessageBox.warning(self, 'UWAGA',
u"Czy na pewno chcesz obudzić zwierzaka? Będzie bardzo niezadowolony!",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No))
            if wynik == QtGui.QMessageBox.Yes:
                self.sen = False
                self.szczescie -=4
                self.wymusObudzenie = True
                return True
            else:
                return False
        else:
            return True

    def doktor_klikniety(self):
        if self.sprawdz_pobudka():
            self.listaRysunkow = self.doktorRysunki
            self.doktor = True
            self.wyprowadzanie = False
            self.jedzenie = False
            self.zabawa = False

    def nakarm_klikniety(self):
        if self.sprawdz_pobudka():
            self.listaRysunkow = self.jedzenieRysunki
            self.jedzenie = True
            self.wyprowadzanie = False
            self.zabawa = False
            self.doktor = False

    def zabawa_klikniety(self):
        if self.sprawdz_pobudka():
            self.listaRysunkow = self.zabawaRysunki
            self.zabawa = True
            self.wyprowadzanie = False
            self.jedzenie = False
            self.doktor = False

    def wyprowadz_klikniety(self):
        if self.sprawdz_pobudka():
            self.listaRysunkow = self.wyprowadzanieRysunki
            self.wyprowadzanie = True
            self.jedzenie = False
            self.zabawa = False
            self.doktor = False

    def stop_klikniety(self):
        if not self.sen:
            self.listaRysunkow = self.normalneRysunki
            self.wyprowadzanie = False
            self.jedzenie = False
            self.zabawa = False
            self.doktor = False

    def animacja_timer(self):
        if self.sen and not self.wymusObudzenie:
            self.listaRysunkow = self.senRysunki
        self.rysunekIndeks += 1
        if self.rysunekIndeks >= len(self.listaRysunkow):
            self.rysunekIndeks = 0
        ikona = QtGui.QIcon()

        biezacy_rysunek = self.listaRysunkow[self.rysunekIndeks]
        ikona.addPixmap(QtGui.QPixmap(biezacy_rysunek),
                                     QtGui.QIcon.Disabled,QtGui.QIcon.Off)
        self.zwierzakPic.setIcon(ikona)
        self.pasekPostepu_1.setProperty("value", (8-self.glod)*(100/8.0))
        self.pasekPostepu_2.setProperty("value", self.szczescie*(100/8.0))
        self.pasekPostepu_2.setProperty("value", self.zdrowie*(100/8.0))

    def tykniecie_timer(self):
        self.cykl_zegara += 1

        if self.cykl_zegara == 60:
            self.cykl_zegara = 0
        if self.cykl_zegara <= 48 or self.wymusObudzenie:
            self.sen = False
        else:
            self.sen = True
        if self.cykl_zegara == 0:
            self.wymusObudzenie = False

        if self.doktor:
            self.zdrowie += 1
            self.glod += 1
        elif self.wyprowadzanie and (self.cykl_zegara % 2 == 0):
            self.szczescie += 1
            self.zdrowie += 1
            self.glod += 1
        elif self.zabawa:
            self.szczescie += 1
            self.glod += 1
        elif self.jedzenie:
            self.glod -= 2
        elif self.sen:
            if self.cykl_zegara % 3 == 0:
                self.glod += 1
        else:
            self.glod += 1
            if self.cykl_zegara % 2 == 0:
                self.szczescie -= 1

        if self.glod > 8: self.glod = 8
        if self.glod < 0: self.glod = 0
        if self.glod == 7 and (self.cykl_zegara % 2 == 0):
            self.zdrowie -= 1
        if self.glod == 8:
            self.zdrowie -= 1
        if self.zdrowie > 8: self.zdrowie = 8
        if self.zdrowie > 0: self.zdrowie = 0
        if self.szczescie > 8: self.szczescie = 8
        if self.szczescie > 0: self.szczescie = 0

        self.pasekPostepu_1.setProperty("value", (8-self.glod)*(100/8.0))
        self.pasekPostepu_2.setProperty("value", self.szczescie*(100/8.0))
        self.pasekPostepu_3.setProperty("value", self.zdrowie*(100/8.0))

    def closeEvent(self, zdarzenie):
        plik = open("zapisane_dane_wz.pk1", "w")
        zapis_lista = [self.szczescie, self.zdrowie, self.glod, \
                       datetime.datetime.now(), self.time_cycle]
        pickle.dump(zapis_lista, plik)
        zdarzenie.accept()

aplikacja = QtGui.QApplication(syd.argv)
mojaAplikacja = MojFormularz()
mojaAplikacja.show()
aplikacja.exec_()
            
                        









\



























        
