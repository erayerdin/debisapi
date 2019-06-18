# DEBİS API

Dokuz Eylül Üniversitesi, DEBİS sistemi için
oluşturulmuş bir API'dır.

# Güvenlik Sistemi

DEBİS API, ayarlardan belirlenen süre boyunca
geçerli olan bir token ile güvenlik doğrulaması
yapmaktadır.

# Uçnoktalar

Her sürüm, kendi uçnoktasını barındırmaktadır.
Şu an sadece `/v1` uçnoktası bulunmaktadır.

Doğrulama uçnoktaları dışındaki tüm uçnoktalar
`Authorization` üstbilgisi (header) istemektedir.
Bu üstbilginin içeriği `Token abc` şeklinde
olmalıdır.

## Doğrulama

| Uçnokta      | Parametre | Eylem | İstek Verisi         |
| ------------ | --------- | ----- | -------------------- |
| /auth/claim/ | -         | POST  | username<br>password |

## Ders Programı

| Uçnokta            | Parametre        | Eylem | İstek Verisi |
| ------------------ | ---------------- | ----- | ------------ |
| /curriculum/       | weekId<br>termId | GET   | -            |
| /curriculum/weeks/ | termId           | GET   | -            |
| /curriculum/terms/ | -                | GET   | -            |

## Sonuçlar

| Uçnokta         | Parametre        | Eylem | İstek Verisi |
| --------------- | ---------------- | ----- | ------------ |
| /results/       | weekId<br>termId | GET   | -            |
| /results/weeks/ | termId           | GET   | -            |
| /results/terms/ | -                | GET   | -            |

# Lisans

Bu yazılım, Apache License 2.0 altında
lisanslanmıştır. Okumak için
[buraya tıklayın](LICENSE.txt) ya da özetini
incelemek için
[şuraya gözatın][tldr_apache].

[tldr_apache]: https://tldrlegal.com/license/apache-license-2.0-(apache-2.0)
