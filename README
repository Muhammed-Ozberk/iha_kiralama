# Air Vehicle Management System

## Proje Tanımı
Air Vehicle Management System (AVMS), uçak ve parçalarının yönetildiği, kullanıcıların uçak ve parçaları kolayca oluşturup listeleyebileceği bir web uygulamasıdır. Bu sistem, yöneticilerin hava araçlarını yönetmesi ve her bir hava aracına ait parçaları düzenlemesi için kullanılır. Django web framework'ü kullanılarak geliştirilmiştir.

---

## Özellikler

### Accounts
- Kullanıcı girişi yönetildi.
- Admin kullanıcı yetkilendirme ve yönetim ekranı oluşturuldu.
- Takım ve izin yönetimi yapıldı.
  - Her takım kendi parçasını üretebilir.
- Admin kullanıcı paneline `/admin` adresi üzerinden erişilebilir.

### Aircrafts (Hava Araçları)
- Hava araçları için CRUD (Create, Read, Update, Delete) işlemleri gerçekleştirildi.
- Hava araçları ve ilgili veriler DataTable kullanılarak listelendi.
- Migration kullanılarak hava araçlarına ait veri seeder oluşturuldu.
- Uçak modelleri kaydedildi.

### Parts (Parçalar)
- Hava araçlarına ait parçaların yönetimi sağlandı.
- Parçalar DataTable ile listelendi ve düzenlendi.
- Migration kullanılarak parça tipleri için veri seeder oluşturuldu.

### UI (Kullanıcı Arayüzü)
- Kullanıcı arayüzü tamamen modern bir tasarımla oluşturuldu.
- Swagger entegrasyonu yapıldı, `/swagger` adresinden erişilebilir.
- Ajax kullanılarak istekler gerçekleştirildi.
- Docker kullanılarak projeyi kolayca çalıştırmak için yapılandırıldı.
  - Çalıştırmak için gerekli komutlar aşağıda verilmiştir.

---

## Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki gereksinimlere ihtiyacınız olacak:

- [Python](https://www.python.org/downloads/) 3.8 veya üzeri
- [Docker](https://www.docker.com)
- Django Framework
- PostgreSQL

---

## Proje Kurulumu

### 1. Docker Kurulumu
Projeyi Docker ile çalıştırmak için aşağıdaki komutları çalıştırın:

```bash
chmod +x wait-for.sh  # Shell dosyasına izin verin
./wait-for.sh         # Gerekli beklemeleri sağlayın
docker-compose up -d  # Docker konteynerlerini başlatın
```

### 2. Sanal Ortam Kurulumu
Docker dışında bir kurulum tercih ederseniz:

```bash
python3 -m venv env   # Sanal ortam oluşturun
source env/bin/activate # Sanal ortamı aktif edin
```

### 3. Bağımlılıkların Yüklenmesi

```bash
pip install -r requirements.txt
```

### 4. Veritabanı Yapılandırması
Django'nun veritabanı ayarlarını `settings.py` dosyasındaki `DATABASES` kısmında yapılandırın ve ardından veritabanını oluşturun:

```bash
python manage.py migrate
```

### 5. Veritabanına Varsayılan Verilerin Eklenmesi
Veri seeder'larını çalıştırarak varsayılan verileri ekleyin:

```bash
python manage.py loaddata initial_data.json
```

### 6. Projenin Çalıştırılması

```bash
python manage.py runserver
```

### 7. Uygulamaya Erişim
Proje çalıştırıldıktan sonra tarayıcınızdan [http://127.0.0.1:8000/](http://127.0.0.1:8000/) adresine giderek uygulamayı kullanabilirsiniz.

---

## Geliştirme Ortamı

Bu proje için kullanılan teknolojiler ve araçlar:

- **Python**: Web uygulama geliştirme için kullanılan ana dil.
- **Django**: Web framework'ü, ORM ve yönetim paneli desteği.
- **HTML/CSS/JavaScript**: Kullanıcı arayüzü için kullanılan temel teknolojiler.
- **jQuery**: Ajax istekleri ve DOM manipülasyonu için kullanıldı.
- **Bootstrap**: Modern ve duyarlı bir arayüz sağlamak için kullanıldı.
- **DataTables**: Tablo verilerini yönetmek ve görüntülemek için kullanıldı.

---

## Swagger ve API
API dokümantasyonu Swagger ile sağlanmıştır. Proje çalıştırıldıktan sonra Swagger arayüzüne `/swagger` adresinden ulaşabilirsiniz.

---

## Ek Bilgiler
- Sadece admin kullanıcı yeni kullanıcı ekleyebilir.
- Tüm gerekli kütüphaneler `requirements.txt` dosyasında listelenmiştir.
- Docker ortamında tüm ayarlar önceden yapılandırılmıştır, ekstra kurulumlara gerek yoktur.
