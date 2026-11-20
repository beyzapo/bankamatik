# Bankamatik Sistemi: PIN ile giriş, bakiye, para yatırma/çekme, işlem geçmişi

GUNLUK_LIMIT = 2000  # sabit: bir seferde çekilebilecek en yüksek tutar (TL)

class Hesap:
    """Banka hesabı: bakiyeyi ve yapılan işlemlerin geçmişini tutar."""
    def __init__(self, hesap_no, bakiye=0):  # nesne oluşturulunca otomatik çalışır
        self.hesap_no = hesap_no  # hesabı tanımlayan numara (örn. TR001)
        self.bakiye = bakiye      # hesaptaki para; verilmezse 0 TL ile başlar
        self.gecmis = []          # her işlem buraya metin olarak eklenir

    def para_yatir(self, tutar):  # hesaba para ekler
        self.bakiye += tutar                          # bakiyeyi tutar kadar artır
        self.gecmis.append(f"+{tutar} TL yatırıldı")  # işlemi geçmişe kaydet
        print(f"{tutar} TL yatırıldı. Yeni bakiye: {self.bakiye} TL")

    def para_cek(self, tutar):  # koşullar sırayla kontrol edilir: önce limit, sonra bakiye
        if tutar > GUNLUK_LIMIT:     # 1) limit aşılıyorsa işlem yapılmaz
            print(f"Tek seferde en fazla {GUNLUK_LIMIT} TL çekebilirsiniz.")
        elif tutar > self.bakiye:    # 2) hesapta yeterli para yoksa işlem yapılmaz
            print("Yetersiz bakiye!")
        else:                        # 3) iki kontrol de geçildiyse para çekilir
            self.bakiye -= tutar                      # bakiyeyi tutar kadar azalt
            self.gecmis.append(f"-{tutar} TL çekildi")  # işlemi geçmişe kaydet
            print(f"{tutar} TL çekildi. Kalan bakiye: {self.bakiye} TL")

    def bakiye_goster(self):  # güncel bakiyeyi ekrana yazar
        print(f"Hesap {self.hesap_no} bakiyesi: {self.bakiye} TL")

    def gecmis_goster(self):  # yapılan tüm işlemleri sırayla listeler
        # Liste boşsa "or" sayesinde bilgi mesajı yazdırılır
        for islem in self.gecmis or ["Henüz işlem yapılmadı."]:
            print("-", islem)

class Kullanici:
    """Banka müşterisi: adı, PIN'i ve sahip olduğu hesabı tutar."""
    def __init__(self, ad, pin, hesap):
        self.ad = ad        # ekranda gösterilecek isim
        self.pin = pin      # giriş için gereken 4 haneli şifre (metin olarak)
        self.hesap = hesap  # Kullanıcı bir Hesap nesnesine sahiptir (has-a ilişkisi)

    def pin_dogrula(self, girilen_pin):  # PIN doğruysa True, yanlışsa False döner
        return self.pin == girilen_pin

def giris_yap(kullanicilar):
    """Kullanıcı adı ve PIN ister; 3 hatalı PIN'de kartı bloke eder."""
    # .lower() ile "Ayse" ve "ayse" aynı kabul edilir; .get() yoksa None döndürür
    kullanici = kullanicilar.get(input("Kullanıcı adı: ").lower())
    if kullanici is None:  # sözlükte böyle bir kullanıcı yok
        print("Kullanıcı bulunamadı.")
        return None
    for kalan_hak in range(2, -1, -1):  # 3 deneme: kalan hak 2, 1, 0
        if kullanici.pin_dogrula(input("PIN: ")):
            print(f"Hoş geldiniz, {kullanici.ad}!")
            return kullanici  # doğru PIN: kullanıcı nesnesini geri ver
        print(f"Hatalı PIN. Kalan hak: {kalan_hak}")
    print("3 kez hatalı PIN girildi. Kartınız bloke edildi.")  # döngü bitti = hak kalmadı
    return None

def tutar_al():
    """Kullanıcıdan pozitif tam sayı alır; geçersizse None döndürür."""
    giris = input("Tutar (TL): ")  # input() her zaman metin (str) döndürür
    if not giris.isdigit() or int(giris) == 0:  # harf, eksi sayı veya 0 girildiyse
        print("Geçersiz tutar! Pozitif bir tam sayı girin.")
        return None
    return int(giris)  # metni sayıya çevirip geri ver

def menu_goster():  # menüyü yazar, kullanıcının seçimini metin olarak döndürür
    return input("\n1) Bakiye  2) Para yatır  3) Para çek  4) Geçmiş  5) Çıkış\nSeçiminiz: ")

def main():  # programın ana akışı: Giriş -> İşlem -> Çıkış
    # Örnek kullanıcılar (gerçek bir sistemde veritabanından gelirdi)
    kullanicilar = {"ayse": Kullanici("Ayşe", "1234", Hesap("TR001", 1500)),
                    "mehmet": Kullanici("Mehmet", "4321", Hesap("TR002", 300))}
    kullanici = giris_yap(kullanicilar)  # 1) GİRİŞ
    if kullanici is None:
        return  # giriş başarısızsa program biter
    hesap = kullanici.hesap  # işlemler giriş yapan kullanıcının hesabında yapılır
    while True:  # 2) İŞLEM: kullanıcı "Çıkış" diyene kadar menü tekrar gösterilir
        secim = menu_goster()
        if secim == "1":
            hesap.bakiye_goster()
        elif secim == "2" or secim == "3":  # iki işlem de tutar istediği için birlikte
            tutar = tutar_al()
            if tutar is None:
                continue  # geçersiz tutarda menüye geri dön
            elif secim == "2":
                hesap.para_yatir(tutar)
            else:
                hesap.para_cek(tutar)
        elif secim == "4":
            hesap.gecmis_goster()
        elif secim == "5":  # 3) ÇIKIŞ
            print("Kartınızı almayı unutmayın. İyi günler!")
            break  # while döngüsünden çıkar, program biter
        else:  # 1-5 dışında bir şey yazıldıysa
            print("Geçersiz seçim, 1-5 arası bir sayı girin.")

if __name__ == "__main__":  # dosya doğrudan çalıştırılınca main() başlar
    main()