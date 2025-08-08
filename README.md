# CAN Bus Message Sender with DBC Support

Bu proje, **CAN bus** üzerinden **DBC dosyası** kullanarak mesaj gönderme işlevi sağlar.  
Kullanıcı arayüzü üzerinden mesaj ve sinyaller seçilir, `value` değeri girilir ve CAN bus'a gönderilir.

## Özellikler
- DBC dosyasından mesaj ve sinyal bilgilerini yükleme
- Mesaj seçimi, sinyal seçimi ve `value` değeri girme
- Seçilen sinyallere karşılık gelen CAN mesajını oluşturma ve gönderme
- `python-can` kütüphanesi ile donanım üzerinden gönderim desteği

## Kullanılan Teknolojiler
- Python 3.x
- [python-can](https://python-can.readthedocs.io/)
- [cantools](https://cantools.readthedocs.io/)
- PyQt5 (kullanıcı arayüzü)

## Kurulum
Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

## Çalıştırma
Ana programı çalıştırmak için:
```bash
python can_main.py
```

## Dizin Yapısı
```
can_main.py                # Uygulamanın giriş noktası
can_sender.py              # Mesaj gönderme fonksiyonları
can_ui.py                  # Kullanıcı arayüzü
dbc_handler.py             # DBC dosyası yükleme ve sinyal okuma
DBC_fixed_cleaned.dbc      # Örnek DBC dosyası
```

## Lisans
Bu proje kişisel kullanım için geliştirilmiştir.
