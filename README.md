# Öğrenci Bilgi Sistemi (OBS) 🎓

Python, Flask ve Tailwind CSS kullanılarak geliştirilmiş tam teşekküllü, modern ve dinamik bir Öğrenci Bilgi Sistemi (Student Information System) web uygulamasıdır. Sistemde **Admin**, **Akademisyen** ve **Öğrenci** olmak üzere üç farklı yetki seviyesi ve bunlara özel kontrol panelleri bulunmaktadır.

## ✨ Özellikler

### 🛡️ Admin Paneli
- Sisteme yeni öğrenci ve akademisyen hesapları ekleme.
- Yeni dersler oluşturma ve bu derslere sorumlu akademisyen atama.
- Öğrencileri derslere kaydetme.
- İstenmeyen kullanıcıları sistemden güvenli bir şekilde silme (ilişkili tüm kayıtlarıyla birlikte).

### 👨‍🏫 Akademisyen Paneli
- Atanmış olunan dersleri görüntüleme.
- Derse kayıtlı öğrencilerin listesine erişim.
- Not girişi (Vize, Final, Proje, Sunum) yapma.
- **Hızlı Yoklama:** Tek bir tıklamayla seçili öğrencilerin devamsızlık durumunu artırma.
- Detaylı öğrenci profillerini görüntüleme.

### 👨‍🎓 Öğrenci Paneli
- Kayıtlı olunan dersleri ve anlık not durumlarını görüntüleme.
- Not ağırlıklarına göre otomatik hesaplanan **Genel Ortalama (GPA)** takibi.
- Ayrıntılı ders notu ilerleme çubukları (Progress bar) ve harf/durum başarı etiketleri (Geçti / Kaldı).
- Görsel uyarılarla desteklenmiş devamsızlık (Yoklama) takibi.

### 🎨 UI & UX
- Modern, temiz ve tam duyarlı (responsive) tasarım (Tailwind CSS).
- Sadece giriş (Login) ekranında görünen, özel tasarlanmış floral dekoratif köşeler.
- Rol tabanlı akıllı yönlendirmeler ve yetkilendirme.

## 🚀 Teknolojiler
- **Backend:** Python, Flask
- **Veritabanı:** SQLite, Flask-SQLAlchemy
- **Kimlik Doğrulama:** Flask-Login, Werkzeug Security (Şifre Hashleme)
- **Frontend:** HTML5, Tailwind CSS, FontAwesome, Jinja2 Template Engine

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Projeyi Klonlayın:**
   ```bash
   git clone https://github.com/KULLANICI_ADINIZ/obs-projesi.git
   cd obs-projesi
   ```

2. **Gerekli Kütüphaneleri Yükleyin:**
   Eğer projenizde henüz bir sanal ortam (virtual environment) yoksa oluşturmanız tavsiye edilir. Ardından bağımlılıkları yükleyin:
   ```bash
   pip install flask flask-sqlalchemy flask-login
   ```

3. **Uygulamayı Başlatın:**
   ```bash
   python app.py
   ```
   *Not: Uygulama ilk kez çalıştırıldığında veritabanını (obs.db) otomatik olarak oluşturacak ve içerisine test edebilmeniz için varsayılan örnek kullanıcılar ile dersleri ekleyecektir.*

4. **Sisteme Giriş:**
   Tarayıcınızdan `http://127.0.0.1:5000` adresine gidin.
   Aşağıdaki varsayılan test hesaplarıyla sistemi inceleyebilirsiniz (Tüm hesapların şifresi `123456` olarak ayarlanmıştır):
   - **Admin:** `admin`
   - **Akademisyenler:** `hoca1`, `hoca2`
   - **Öğrenciler:** `ogrenci1`, `ogrenci2`

## 🤝 Katkıda Bulunma
Bu proje geliştirilmeye açıktır. Pull request (PR) göndererek ya da issue açarak katkıda bulunabilirsiniz.

## 📜 Lisans
Bu proje MIT Lisansı altında sunulmaktadır.
