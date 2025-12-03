import abc # Python'da Soyut Sınıf (Abstract Class) oluşturmak için gerekli modül.

# 1. ÖZEL HATA YÖNETİMİ (CUSTOM EXCEPTION)
# KuantumCokusuException: Standart hatalar yerine kendi özel hatamızı yazıyoruz.
# Bir nesnenin stabilitesi bittiğinde bu hatayı fırlatarak oyunu bitireceğiz (Game Over).
class KuantumCokusuException(Exception):
    def __init__(self, message):
        super().__init__(message)


# 2. ARAYÜZ (INTERFACE) SİMÜLASYONU
# Python'da 'interface' anahtar kelimesi yoktur. 
# Ancak abc.ABC'den miras alarak ve metodun içini boş bırakarak (pass)
# aynı yapıyı kurabiliriz. Sadece tehlikeli nesneler bunu miras alacak.
class IKritik(abc.ABC):
    @abc.abstractmethod
    def acil_durum_sogutmasi(self):
        pass


# 3. ANA SOYUT SINIF (ABSTRACT CLASS)
#KuantumNesnesi: Tüm maddelerin ortak atası.
# abc.ABC sınıfından türeterek bunun bir Soyut Sınıf olduğunu belirtiyoruz.
class KuantumNesnesi(abc.ABC):
    def __init__(self, id_val, tehlike_seviyesi):
        self.id = id_val #  Nesne Kimliği
        self.tehlike_seviyesi = tehlike_seviyesi #  1-10 arası tehlike puanı
        self._stabilite = 100.0 # Başlangıçta depo full

    # ENCAPSULATION (KAPSÜLLEME) - Getter
    # Stabilite değişkenine doğrudan erişimi engelliyoruz, bu property ile okuyoruz.
    @property
    def stabilite(self):
        return self._stabilite

    # ENCAPSULATION - Setter (Kontrol Mekanizması)
    # Değer atanırken araya girip 0-100 kontrolü yapıyoruz.
    @stabilite.setter
    def stabilite(self, value):
        if value > 100:
            self._stabilite = 100
        #  OYUN BİTİRİCİ KONTROL
        # Eğer stabilite 0 veya altına düşerse, sessizce kalma; HATA FIRLAT!
        elif value <= 0: 
            self._stabilite = 0
            # Bu hata fırlatıldığında kodun akışı durur ve 'except' bloğuna gider.
            raise KuantumCokusuException(f"{self.id} isimli nesne kararsızlaştı ve PATLADI!")
        else:
            self._stabilite = value

    # Soyut Metot (Abstract Method)
    # @abc.abstractmethod dekoratörü, alt sınıfların bu metodu
    # MUTLAKA kendine göre doldurmasını (Override) zorunlu kılar.
    @abc.abstractmethod
    def analiz_et(self):
        pass

    # Ortak Metot: Durum Bilgisi Raporlama
    def durum_bilgisi(self):
        return f"ID: {self.id} | Stabilite: %{self.stabilite} | Tehlike: {self.tehlike_seviyesi}"

# 4. NESNE ÇEŞİTLERİ (INHERITANCE & POLYMORPHISM)

# A. Veri Paketi (Masum Nesne)
# IKritik DEĞİLDİR, yani soğutulamaz.
class VeriPaketi(KuantumNesnesi):
    def __init__(self, id_val):
        super().__init__(id_val, 1) # Tehlike seviyesi: 1 (Düşük)
        
    def analiz_et(self):
        # Polimorfizm: Sadece 5 birim hasar alır.
        self.stabilite -= 5
        print("Veri içeriği okundu.")

# B. Karanlık Madde (Tehlikeli Nesne)
# Hem KuantumNesnesi'nden hem de IKritik'ten miras alır (Multiple Inheritance).
class KaranlikMadde(KuantumNesnesi, IKritik):
    def __init__(self, id_val):
        super().__init__(id_val, 5) # Tehlike seviyesi: 5 (Orta)

    def analiz_et(self):
        #15 birim hasar alır.
        self.stabilite -= 15

    # Interface Metodu: Soğutma
    def acil_durum_sogutmasi(self):
        # +50 can yenilenir.
        temp = self.stabilite + 50
        if temp > 100: temp = 100
        self.stabilite = temp # Setter tetiklenir
        print(f"{self.id} soğutuldu. Yeni Stabilite: {self.stabilite}")

# C. Anti Madde (Çok Tehlikeli Nesne)
# IKritik miras alır.
class AntiMadde(KuantumNesnesi, IKritik):
    def __init__(self, id_val):
        super().__init__(id_val, 10) # Tehlike seviyesi: 10 (Yüksek)

    def analiz_et(self):
        # Çok hızlı hasar alır (25 birim).
        self.stabilite -= 25
        print("Evrenin dokusu titriyor...") # [cite: 40]

    def acil_durum_sogutmasi(self):
        temp = self.stabilite + 50
        if temp > 100: temp = 100
        self.stabilite = temp
        print(f"{self.id} için kritik soğutma uygulandı.")

# 5. OYUN DÖNGÜSÜ (MAIN LOOP)
def main():
    # Envanter Listesi (Polimorfizm için farklı türleri burada tutacağız)
    envanter = []

    print("SİSTEM BAŞLATILIYOR (PYTHON)...")

    #Sonsuz Döngü: Kullanıcı çıkış diyene kadar döner.
    while True:
        print("\n=== OMEGA SEKTÖRÜ (PYTHON) ===")
        print("1. Yeni Nesne Ekle")
        print("2. Tüm Envanteri Listele")
        print("3. Nesneyi Analiz Et")
        print("4. Acil Durum Soğutması Yap")
        print("5. Çıkış")
        
        secim = input("Seçiminiz: ")

        # Hata Yakalama (Exception Handling) Bloğu
        try:
            if secim == "1":
                print("\nTip Seç: (1) Veri, (2) Karanlık Madde, (3) Anti Madde")
                tip = input("Tip: ")
                yeni_id = input("Nesne ID: ")
                
                # Factory Pattern Benzeri Nesne Üretimi
                if tip == "1":
                    envanter.append(VeriPaketi(yeni_id))
                elif tip == "2":
                    envanter.append(KaranlikMadde(yeni_id))
                elif tip == "3":
                    envanter.append(AntiMadde(yeni_id))
                else:
                    print("Geçersiz tip.")
                
                if tip in ["1", "2", "3"]:
                    print(f"{yeni_id} eklendi.")

            elif secim == "2":
                print("\n--- Envanter Raporu ---")
                # POLİMORFİZM:
                # Listenin içinde farklı nesneler olsa da hepsi 'durum_bilgisi' metoduna sahip.
                for nesne in envanter:
                    print(nesne.durum_bilgisi())

            elif secim == "3":
                analiz_id = input("\nAnaliz edilecek ID: ")
                # Listeden ID'ye göre bulma (Pythonic way)
                bulunan = next((x for x in envanter if x.id == analiz_id), None)
                
                if bulunan:
                    # DİKKAT: Analiz sırasında nesne patlayabilir!
                    # Eğer patlarsa KuantumCokusuException fırlar ve 'except' bloğuna gideriz.
                    bulunan.analiz_et() 
                    print(f"Güncel Stabilite: %{bulunan.stabilite}")
                else:
                    print("Nesne bulunamadı!")

            elif secim == "4":
                soguk_id = input("\nSoğutulacak ID: ")
                bulunan = next((x for x in envanter if x.id == soguk_id), None)

                # TYPE CHECKING (TÜR KONTROLÜ)
                # Nesne IKritik sınıfından mı türetilmiş? (isinstance)
                if isinstance(bulunan, IKritik):
                    bulunan.acil_durum_sogutmasi()
                elif bulunan:
                    # Kritik değilse hata ver.
                    print("HATA: Bu nesne soğutulamaz! (IKritik değil)")
                else:
                    print("Nesne bulunamadı.")

            elif secim == "5":
                print("Çıkış yapılıyor...")
                break
            else:
                print("Geçersiz seçim.")

        # GAME OVER YAKALAMA
        # KuantumCokusuException yakalanırsa oyun biter.
        except KuantumCokusuException as ex:
            print("\n" + "*"*40)
            print("SİSTEM ÇÖKTÜ! TAHLİYE BAŞLATILIYOR...")
            print(f"SEBEP: {ex}") # Hata mesajını yazdır
            print("*"*40 + "\n")
            break # Döngüyü kırar ve program sonlanır.
        
        # Beklenmedik diğer hatalar için
        except Exception as e:
            print(f"Beklenmedik hata: {e}")

# Programı başlatma noktası
if __name__ == "__main__":
    main()