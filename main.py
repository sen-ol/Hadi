import datetime
from datetime import date

import pyrebase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout

Window.size = (480, 800)


class HadiKart(FakeRectangularElevationBehavior, MDFloatLayout):
    isim = StringProperty()
    aciklama = StringProperty()


class Hadi(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        firebaseConfig = {
            "apiKey": "AIzaSyCmDwDRshOShV-jLIrios1T8ev6344MKQs",
            "authDomain": "hadi-ac6cb.firebaseapp.com",
            'databaseURL': "https://hadi-ac6cb-default-rtdb.firebaseio.com",
            "projectId": "hadi-ac6cb",
            "storageBucket": "hadi-ac6cb.appspot.com",
            "messagingSenderId": "150681684050",
            "appId": "1:150681684050:web:7ebaf7f6033d3c9b65b78b"
        }
        firebase = pyrebase.initialize_app(firebaseConfig)

        # veri setini yarat
        self.veriler = firebase.database()

    def ekran_degistir(self, ekran_ismi):
        ekran_yoneticisi.current_screen = ekran_ismi

    def build(self):
        global ekran_yoneticisi
        ekran_yoneticisi = ScreenManager()
        ekran_yoneticisi.add_widget(Builder.load_file("hadi.kv"))
        ekran_yoneticisi.add_widget(Builder.load_file("hadilerim.kv"))
        ekran_yoneticisi.add_widget(Builder.load_file("hadi_ekle.kv"))
        ekran_yoneticisi.add_widget(Builder.load_file("adim_at.kv"))
        ekran_yoneticisi.add_widget(Builder.load_file("tamamla.kv"))

        return ekran_yoneticisi

    def on_start(self):
        today = date.today()
        self.hafta_ici_gunleri = date.weekday(today)
        self.days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
        self.year = str(datetime.datetime.now().year)
        self.month = str(datetime.datetime.now().strftime("%b"))
        self.day = str(datetime.datetime.now().strftime("%d"))

        self.tarih = f"{self.day}, {self.month}, {self.year}, {self.days[self.hafta_ici_gunleri]}"

        ekran_yoneticisi.get_screen("AnaEkran").ids.an.text = self.tarih

        veri_seti = self.veriler.get()

        if veri_seti.val() is not None:
            for single_data in veri_seti.each():
                veri_dict = single_data.val()
                if veri_dict["Hadi_ismi"] != "":
                    baslangic_hadi_listesi = veri_dict["Hadi_ismi"]
                    ekran_yoneticisi.get_screen("Hadilerim").hadi_listesi.add_widget(
                        HadiKart(isim=veri_dict["Hadi_ismi"],
                                 aciklama=veri_dict["Hadi_Bilgi"]))

    def on_complete(self, checkbox, value, isim, aciklama, bar):
        if value:
            isim.text = isim = f"[s]{isim.text}[/s]"
            aciklama.text = aciklama = f"[s]{aciklama.text}[/s]"
            bar.md_bg_color = 0, 179/255, 0, 1
        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                isim.text = isim.text.replace(i, "")
                aciklama.text = aciklama.text.replace(i, "")
                bar.md_bg_color = 1, 170/255, 23/255, 1


    def hadi_ekle(self, hadi_girilen_isim, hadi_girilen_bilgi):
        hadi_ismi = hadi_girilen_isim
        hadi_bilgi = hadi_girilen_bilgi
        yapilma_durumu = False
        eklenen_zaman = self.tarih

        veri = {"Hadi_ismi": hadi_ismi, "Hadi_Bilgi": hadi_bilgi, "Eklenen_Zaman": eklenen_zaman, "Durum": yapilma_durumu}

        print(veri)
        self.veriler.child(hadi_ismi).set(veri)


Hadi().run()
