# Bankamatik Sistemi: PIN ile giriş, bakiye, para yatırma/çekme, işlem geçmişi

GUNLUK_LIMIT = 2000  # bir seferde çekilebilecek en yüksek tutar (TL)

class Hesap:
    """Banka hesabı: bakiyeyi ve yapılan işlemlerin geçmişini tutar."""
    def __init__(self, hesap_no, bakiye=0):
        self.hesap_no = hesap_no
        self.bakiye = bakiye
        self.gecmis = []  # her işlem buraya metin olarak eklenir

    def para_yatir(self, tutar):
        self.bakiye += tutar
        self.gecmis.append(f"+{tutar} TL yatırıldı")
        print(f"{tutar} TL yatırıldı. Yeni bakiye: {self.bakiye} TL")

    def para_cek(self, tutar):
        # Koşullar: limit aşılırsa veya bakiye yetmezse işlem yapılmaz
        if tutar > GUNLUK_LIMIT:
            print(f"Tek seferde en fazla {GUNLUK_LIMIT} TL çekebilirsiniz.")
        elif tutar > self.bakiye:
            print("Yetersiz bakiye!")
        else:
            self.bakiye -= tutar
            self.gecmis.append(f"-{tutar} TL çekildi")
            print(f"{tutar} TL çekildi. Kalan bakiye: {self.bakiye} TL")

    def bakiye_goster(self):
        print(f"Hesap {self.hesap_no} bakiyesi: {self.bakiye} TL")

    def gecmis_goster(self):
        # Liste boşsa "or" sayesinde bilgi mesajı yazdırılır
        for islem in self.gecmis or ["Henüz işlem yapılmadı."]:
            print("-", islem)

class Kullanici:
    """Banka müşterisi: adı, PIN'i ve sahip olduğu hesabı tutar."""
    def __init__(self, ad, pin, hesap):
        self.ad = ad
        self.pin = pin
        self.hesap = hesap  # Kullanıcı bir Hesap nesnesine sahiptir

    def pin_dogrula(self, girilen_pin):
        return self.pin == girilen_pin

def giris_yap(kullanicilar):
    """Kullanıcı adı ve PIN ister; 3 hatalı PIN'de kartı bloke eder."""
    kullanici = kullanicilar.get(input("Kullanıcı adı: ").lower())
    if kullanici is None:
        print("Kullanıcı bulunamadı.")
        return None
    for kalan_hak in range(2, -1, -1):
        if kullanici.pin_dogrula(input("PIN: ")):
            print(f"Hoş geldiniz, {kullanici.ad}!")
            return kullanici
        print(f"Hatalı PIN. Kalan hak: {kalan_hak}")
    print("3 kez hatalı PIN girildi. Kartınız bloke edildi.")
    return None

def tutar_al():
    """Kullanıcıdan pozitif tam sayı alır; geçersizse None döndürür."""
    giris = input("Tutar (TL): ")
    if not giris.isdigit() or int(giris) == 0:
        print("Geçersiz tutar! Pozitif bir tam sayı girin.")
        return None
    return int(giris)

def menu_goster():
    return input("\n1) Bakiye  2) Para yatır  3) Para çek  4) Geçmiş  5) Çıkış\nSeçiminiz: ")

def main():
    # Örnek kullanıcılar (gerçek bir sistemde veritabanından gelirdi)
    kullanicilar = {"ayse": Kullanici("Ayşe", "1234", Hesap("TR001", 1500)),
                    "mehmet": Kullanici("Mehmet", "4321", Hesap("TR002", 300))}
    kullanici = giris_yap(kullanicilar)
    if kullanici is None:
        return  # giriş başarısızsa program biter
    hesap = kullanici.hesap
    while True:  # kullanıcı "Çıkış" diyene kadar menü tekrar gösterilir
        secim = menu_goster()
        if secim == "1":
            hesap.bakiye_goster()
        elif secim == "2" or secim == "3":
            tutar = tutar_al()
            if tutar is None:
                continue  # geçersiz tutarda menüye geri dön
            elif secim == "2":
                hesap.para_yatir(tutar)
            else:
                hesap.para_cek(tutar)
        elif secim == "4":
            hesap.gecmis_goster()
        elif secim == "5":
            print("Kartınızı almayı unutmayın. İyi günler!")
            break
        else:
            print("Geçersiz seçim, 1-5 arası bir sayı girin.")

if __name__ == "__main__":
    main()