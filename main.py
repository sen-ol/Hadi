import datetime
import os
from datetime import date

import pyrebase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.pickers import MDTimePicker

Window.size = (380, 720)


class HadiKart(CommonElevationBehavior, MDFloatLayout):
    isim = StringProperty()
    aciklama = StringProperty()
    eklenen_tarih = StringProperty()
    avatar = StringProperty()


class AvatarButonu(ButtonBehavior, Image):
    source = StringProperty()


class Hadi(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.secilen_avatar = None

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
        self.auth = firebase.auth()

    def ekran_degistir(self, ekran_ismi):
        ekran_yoneticisi.current_screen = ekran_ismi

    def build(self):
        global ekran_yoneticisi
        ekran_yoneticisi = ScreenManager()
        ekran_yoneticisi.add_widget(Builder.load_file("ekranlar/hosgeldin.kv"))
        ekran_yoneticisi.add_widget(Builder.load_file("ekranlar/giris.kv"))
        ekran_yoneticisi.add_widget(Builder.load_file("ekranlar/kayit.kv"))
        ekran_yoneticisi.add_widget(Builder.load_file("ekranlar/hadi.kv"))
        ekran_yoneticisi.add_widget(Builder.load_file("ekranlar/hadilerim.kv"))
        ekran_yoneticisi.add_widget(Builder.load_file("ekranlar/hadi_ekle.kv"))
        ekran_yoneticisi.add_widget(Builder.load_file("ekranlar/adim_at.kv"))
        ekran_yoneticisi.add_widget(Builder.load_file("ekranlar/tamamla.kv"))

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

        print(type(veri_seti))

        if veri_seti.val() is not None:
            for single_data in veri_seti.each():
                veri_dict = single_data.val()
                if veri_dict["Hadi_ismi"] != "":
                    avatar_source=f"ikonlar/{veri_dict['Avatar']}.png"
                    baslangic_hadi_listesi = veri_dict["Hadi_ismi"]
                    ekran_yoneticisi.get_screen("Hadilerim").hadi_listesi.add_widget(
                        HadiKart(isim=veri_dict["Hadi_ismi"],
                                 aciklama=veri_dict["Hadi_Bilgi"],
                                 eklenen_tarih=veri_dict["Eklenen_Zaman"],
                                 avatar=avatar_source))
                elif veri_dict["Kayit_ismi"] != "":
                    print(veri_dict["Kayit_ismi"])

        folder = 'ikonlar'
        avatar_listesi = os.listdir(folder)

        for file in avatar_listesi:

            # print(file)

            avatar = AvatarButonu(source=f"ikonlar/{file}")

            ekran_yoneticisi.get_screen("Hadi_Ekle").avatar_listesi.add_widget(avatar)



    def avatar_secildi(self, dosya_ismi):

        secilen_dosya = os.path.basename(dosya_ismi.source)

        self.secilen_avatar = os.path.splitext(secilen_dosya)[0]

        ekran_yoneticisi.get_screen("Hadi_Ekle").avatar_secildi_popup.text = f"{self.secilen_avatar} seçildi"




        """try:
            self.ids.avatar.source = dosya_ismi[0]
            print(dosya_ismi[0])
        except:
            pass"""

    def on_complete(self, checkbox, value, isim, aciklama, bar):
        if value:
            isim.text = isim = f"[s]{isim.text}[/s]"
            aciklama.text = aciklama = f"[s]{aciklama.text}[/s]"
            # eklenen_tarih.text = eklenen_tarih = f"[s]{eklenen_tarih.text}[/s]"
            bar.md_bg_color = 0, 179 / 255, 0, 1
        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                isim.text = isim.text.replace(i, "")
                aciklama.text = aciklama.text.replace(i, "")
                # eklenen_tarih.text = eklenen_tarih.text.replace(i, "")
                bar.md_bg_color = 1, 170 / 255, 23 / 255, 1

    def hadi_ekle(self, hadi_ismi, hadi_bilgi):
        yapilma_durumu = False
        eklenen_zaman = self.tarih

        veri = {"Hadi_ismi": hadi_ismi, "Hadi_Bilgi": hadi_bilgi, "Eklenen_Zaman": eklenen_zaman,
                "Durum": yapilma_durumu, "Avatar": self.secilen_avatar}

        self.veriler.child(hadi_ismi).set(veri)

        ekran_yoneticisi.get_screen("Hadi_Ekle").hadi_girilen_bilgi.text = ""
        ekran_yoneticisi.get_screen("Hadi_Ekle").hadi_girilen_isim.text = ""

    """def avatar_secildi(self):
        ekran_yoneticisi.get_screen("Hadi_Ekle").avatar_secildi_popup.text = "Avatar seçildi"
"""

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

        MDTimePicker(
            primary_color="orange",
            accent_color="green",
            text_button_color="white",
        ).open()

    def get_time(self, instance, time):
        '''
        The method returns the set time.

        :type instance: <kivymd.uix.picker.MDTimePicker object>
        :type time: <class 'datetime.time'>
        '''

        ekran_yoneticisi.get_screen("adim_at").bitis_saati.text = str(time)

        print(time)

        return time

    def kayit_ol(self, kayit_isim, kayit_email, kayit_sifre):
        self.auth.create_user_with_email_and_password(kayit_email, kayit_sifre)

        veri = {"Kayit_ismi": kayit_isim, "Kayit_Email": kayit_email, "Kayit_Sifre": kayit_sifre}

        self.veriler.child(kayit_isim).set(veri)

        print(veri)




        ekran_yoneticisi.get_screen("Kayit_Ekrani").ids.kayit_isim.text = ""
        ekran_yoneticisi.get_screen("Kayit_Ekrani").ids.kayit_email.text = ""
        ekran_yoneticisi.get_screen("Kayit_Ekrani").ids.kayit_sifre.text = ""

        ekran_yoneticisi.current = "Giris_Ekrani"


    def giris_yap(self, email, sifre):
        try:
            self.auth.sign_in_with_email_and_password(email, sifre)

            ekran_yoneticisi.get_screen("Giris_Ekrani").ids.giris_email.text = ""
            ekran_yoneticisi.get_screen("Giris_Ekrani").ids.giris_sifre.text = ""

            ekran_yoneticisi.current = "AnaEkran"

            giris_yapan = self.auth.current_user
            print(giris_yapan)

        except:
            print("Giriş başarısız!")



Hadi().run()
