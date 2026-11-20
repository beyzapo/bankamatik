# Bankamatik Sistemi

Python ile yazılmış, konsolda çalışan basit bir ATM (bankamatik) uygulaması. Kullanıcı PIN ile giriş yapar; bakiye sorgulayabilir, para yatırıp çekebilir ve işlem geçmişini görebilir.

## Nasıl Çalıştırılır?

### 1. Gereksinim

Bilgisayarda **Python 3** kurulu olmalı. Ek bir kütüphane gerekmez. Kurulu olup olmadığını terminalde kontrol edin:

```bash
python --version
```

`Python 3.x.x` yazıyorsa hazırsınız. Hata alırsanız [python.org](https://www.python.org/downloads/) adresinden indirip kurun. Windows'ta kurulumda **"Add Python to PATH"** kutusunu işaretleyin.

### 2. Projeyi indirme

**Git ile:**

```bash
git clone https://github.com/beyzapo/bankamatik.git
cd bankamatik
```

**Git olmadan:** Repo sayfasında **Code → Download ZIP**'e tıklayın, ZIP'i açın ve terminalde o klasöre gidin (`cd klasor_yolu`).

### 3. Programı başlatma

```bash
python bankamatik.py
```

Windows'ta `python` komutu çalışmazsa `py bankamatik.py`, macOS/Linux'ta ise `python3 bankamatik.py` deneyin.

VS Code kullanıyorsanız `bankamatik.py` dosyasını açıp sağ üstteki **▶ (Run Python File)** butonuna da basabilirsiniz.

### 4. Kullanım

1. `Kullanıcı adı:` sorusuna aşağıdaki tablodan bir ad yazıp Enter'a basın.
2. `PIN:` sorusuna o kullanıcının PIN'ini yazın.
3. Menüde yapmak istediğiniz işlemin numarasını (1–5) yazıp Enter'a basın.
4. Programdan çıkmak için `5`'i seçin. Programı istediğiniz an durdurmak için `Ctrl + C` tuşlarına basabilirsiniz.

Deneme için tanımlı kullanıcılar:

| Kullanıcı adı | PIN | Başlangıç bakiyesi |
| --- | --- | --- |
| ayse | 1234 | 1500 TL |
| mehmet | 4321 | 300 TL |

## Dosyalar

| Dosya | İçerik |
| --- | --- |
| `bankamatik.py` | Programın kaynak kodu (100 satır) |

## Sınıflar neden böyle tasarlandı?

Gerçek hayatta bir banka müşterisi ile onun banka hesabı farklı şeylerdir. Kodda da bu iki kavram ayrı sınıflara bölündü.

| Sınıf | Attribute'lar | Metotlar | Görevi |
| --- | --- | --- | --- |
| `Hesap` | `hesap_no`, `bakiye`, `gecmis` | `para_yatir()`, `para_cek()`, `bakiye_goster()`, `gecmis_goster()` | Parayla ilgili her şeyi yönetir |
| `Kullanici` | `ad`, `pin`, `hesap` | `pin_dogrula()` | Kimlik bilgisini tutar ve doğrular |

- **Sorumluluk ayrımı:** Parayla ilgili işlemler yalnızca `Hesap`'ta, kimlik kontrolü yalnızca `Kullanici`'da yapılır. Bir kuralı değiştirmek gerektiğinde hangi sınıfa bakılacağı bellidir.
- **İlişki (has-a):** `Kullanici` bir `Hesap` nesnesine sahiptir (`self.hesap`). Giriş yapan kullanıcının hesabına `kullanici.hesap` ile ulaşılır.
- **Veri ve davranış bir arada:** Bakiye, `Hesap` nesnesinin içinde tutulur ve yalnızca onun metotlarıyla değiştirilir. Böylece her para hareketi `gecmis` listesine de otomatik olarak kaydedilir.

## Fonksiyonlar hangi amaçla yazıldı?

| Fonksiyon | Amacı |
| --- | --- |
| `giris_yap(kullanicilar)` | Kullanıcı adını ve PIN'i sorar, 3 deneme hakkı verir. Başarılıysa `Kullanici` nesnesini, değilse `None` döndürür. |
| `tutar_al()` | Girilen tutarı doğrular. Geçerliyse sayıyı, değilse `None` döndürür. Hem yatırma hem çekme işleminde kullanıldığı için kod tekrarını önler. |
| `menu_goster()` | Menüyü ekrana yazar ve kullanıcının seçimini döndürür. |
| `main()` | Programın ana akışıdır: kullanıcıları oluşturur, girişi yaptırır ve menü döngüsünü çalıştırır. |

Her fonksiyonun tek bir görevi vardır. Bu sayede kod okunabilir kalır ve her parça ayrı ayrı test edilebilir.

## Koşullar nasıl çalışıyor?

| Yer | Koşul | Sonuç |
| --- | --- | --- |
| `giris_yap` | Kullanıcı sözlükte yoksa (`is None`) | "Kullanıcı bulunamadı" mesajı verilir, program biter |
| `giris_yap` | PIN yanlışsa | Kalan hak azalır. 3 hata sonunda kart bloke edilir. |
| `tutar_al` | Giriş sayı değilse veya 0 ise | Uyarı verilir, menüye dönülür (`continue`) |
| `para_cek` | `tutar > GUNLUK_LIMIT` | Limit uyarısı verilir |
| `para_cek` | `tutar > self.bakiye` | "Yetersiz bakiye" uyarısı verilir |
| `para_cek` | Diğer durumlar (`else`) | Para çekilir, işlem geçmişe yazılır |
| `main` | `if / elif / else` zinciri | Menü seçimine göre doğru metot çağrılır. 1–5 dışındaki girişler "geçersiz seçim" olur. |

`para_cek` içindeki `if / elif / else` sırası önemlidir: önce limit, sonra bakiye kontrol edilir. Para ancak iki kontrol de geçilirse çekilir.

## Programın genel işleyişi

1. **Giriş:** `main()` örnek kullanıcıları oluşturur ve `giris_yap()` fonksiyonunu çağırır.
2. **Doğrulama:** Kullanıcı adı ve PIN kontrol edilir. Başarısız girişte program sona erer.
3. **İşlem:** `while True` döngüsüyle menü tekrar tekrar gösterilir ve seçilen işlem `Hesap` metotlarıyla yapılır.
4. **Çıkış:** Kullanıcı 5'i seçtiğinde `break` ile döngüden çıkılır ve program biter.

## Kullanıcı programı açınca hangi adımları izler?

1. Kullanıcı adını yazar (örnek: `ayse`).
2. PIN'ini girer (örnek: `1234`). En fazla 3 deneme hakkı vardır.
3. Menüden bir işlem seçer:
    - `1` → Bakiyesini görür.
    - `2` → Tutar girip para yatırır.
    - `3` → Tutar girip para çeker (en fazla 2000 TL, bakiyesi kadar).
    - `4` → Yaptığı işlemlerin listesini görür.
    - `5` → Programdan çıkar.
4. Her işlemden sonra menüye geri döner ve `5`'i seçene kadar istediği kadar işlem yapabilir.

## Örnek çıktı

```text
Kullanıcı adı: ayse
PIN: 1234
Hoş geldiniz, Ayşe!

1) Bakiye  2) Para yatır  3) Para çek  4) Geçmiş  5) Çıkış
Seçiminiz: 3
Tutar (TL): 700
700 TL çekildi. Kalan bakiye: 800 TL

1) Bakiye  2) Para yatır  3) Para çek  4) Geçmiş  5) Çıkış
Seçiminiz: 5
Kartınızı almayı unutmayın. İyi günler!
```