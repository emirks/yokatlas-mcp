# YOKATLAS API MCP Sunucusu

[![Star History Chart](https://api.star-history.com/svg?repos=saidsurucu/yokatlas-mcp&type=Date)](https://www.star-history.com/#saidsurucu/yokatlas-mcp&Date)

Bu proje, [YÖKATLAS](https://yokatlas.yok.gov.tr/) verilerine erişimi sağlayan `yokatlas-py` Python kütüphanesini kullanarak bir [FastMCP](https://www.gofastmcp.com/) sunucusu oluşturur. Bu sayede, YÖKATLAS API fonksiyonları, Model Context Protocol (MCP) destekleyen LLM (Büyük Dil Modeli) uygulamaları ve diğer istemciler tarafından araç (tool) olarak kullanılabilir hale gelir.

![örnek](./ornek.png)

## 🎯 Temel Özellikler

* YÖKATLAS verilerine programatik erişim için standart bir MCP arayüzü.
* Lisans ve Önlisans program detaylarını getirme.
* Lisans ve Önlisans programları için kapsamlı arama yapabilme (Tercih Sihirbazı).
* Claude Desktop uygulaması ile kolay entegrasyon.

## 📋 Ön Gereksinimler

* **Python Sürümü:** Python 3.12 veya daha yeni bir sürümünün sisteminizde kurulu olması gerekmektedir. Python'ı [python.org](https://www.python.org/downloads/) adresinden indirebilirsiniz.
* **pip:** Python ile birlikte gelen `pip` paket yöneticisinin çalışır durumda olması gerekir.

## ⚙️ Kurulum Adımları

### Hızlı Kurulum (Önerilen)

Claude Desktop'a entegre etmek için sadece `uv` kurulumuna ihtiyacınız var:

#### 1. `uv` Kurulumu
`uv`, hızlı bir Python paket yöneticisidir.

* **macOS ve Linux:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

* **Windows (PowerShell):**
  ```bash
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

* **pip ile kurulum:**
  ```bash
  pip install uv
  ```

Kurulumu doğrulayın: `uv --version`

#### 2. Claude Desktop'a Ekleme

Claude Desktop ayarlarından (Settings > Developer > Edit Config) yapılandırma dosyasına aşağıdaki girdiyi ekleyin:

```json
{
  "mcpServers": {
    "YOKATLAS API Servisi": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/saidsurucu/yokatlas-mcp",
        "yokatlas-mcp"
      ]
    }
  }
}
```

### Geliştirici Kurulumu

Projeyi yerel olarak geliştirmek için:

1. **Repoyu klonlayın:**
   ```bash
   git clone https://github.com/saidsurucu/yokatlas-mcp.git
   cd yokatlas-mcp
   ```

2. **Bağımlılıkları kurun:**
   ```bash
   uv pip install -e .
   ```

3. **Test edin:**
   ```bash
   yokatlas-mcp --dev  # Geliştirme modu (HTTP)
   yokatlas-mcp        # Üretim modu (STDIO)
   ```

## 🚀 Claude Desktop Entegrasyonu (Hızlı Kurulum - Önerilen)

Bu sunucuyu Claude Desktop uygulamasına eklemenin en kolay yolu `uvx` komutunu kullanmaktır:

```bash
uvx --from git+https://github.com/saidsurucu/yokatlas-mcp yokatlas-mcp
```

Bu komut, sunucuyu GitHub'dan doğrudan çalıştırır ve Claude Desktop ile MCP protokolü üzerinden iletişim kurar. Tüm bağımlılıklar otomatik olarak yönetilir.

### Alternatif: Yerel Kurulum

Eğer projeyi yerel olarak geliştirmek veya değiştirmek isterseniz:

1. Projeyi klonlayın:
   ```bash
   git clone https://github.com/saidsurucu/yokatlas-mcp.git
   cd yokatlas-mcp
   ```

2. `fastmcp install` ile kurun:
   ```bash
   fastmcp install yokatlas_mcp_server.py --name "YOKATLAS API Servisi"
   ```

Bu komut, sunucuyu Claude Desktop uygulamanıza kalıcı olarak ekleyecektir.

## ⚙️ Claude Desktop Manuel Kurulumu (Yapılandırma Dosyası ile - Alternatif)

Sunucuyu Claude Desktop'a manuel olarak eklemek için yapılandırma dosyasını düzenleyebilirsiniz:

1. **Claude Desktop Ayarlarını Açın:**
   - Settings > Developer > Edit Config

2. **Yapılandırma Dosyasına Ekleyin:**
   ```json
   {
     "mcpServers": {
       "YOKATLAS API Servisi": {
         "command": "uvx",
         "args": [
           "--from",
           "git+https://github.com/saidsurucu/yokatlas-mcp",
           "yokatlas-mcp"
         ]
       }
     }
   }
   ```

3. **Claude Desktop'ı Yeniden Başlatın**

Başarılı bir kurulumdan sonra, Claude Desktop uygulamasında giriş kutusunun sağ alt köşesinde çekiç (🛠️) simgesini ve tıkladığınızda "YOKATLAS API Servisi" araçlarını görmelisiniz.

## 🛠️ Kullanılabilir Araçlar (MCP Tools)

Bu FastMCP sunucusu aşağıdaki araçları sunar:

1.  **`get_associate_degree_atlas_details`**
    * **Açıklama:** Belirli bir önlisans programının (Önlisans Atlası) verilen yıldaki tüm detaylarını getirir.
    * **Parametreler:** `program_id: str`, `year: int`

2.  **`get_bachelor_degree_atlas_details`**
    * **Açıklama:** Belirli bir lisans programının (Lisans Atlası) verilen yıldaki tüm detaylarını getirir.
    * **Parametreler:** `program_id: str`, `year: int`

3.  **`search_bachelor_degree_programs`**
    * **Açıklama:** Çeşitli kriterlere göre lisans programlarını (Lisans Tercih Sihirbazı) arar.
    * **Parametreler:** `uni_adi: str`, `program_adi: str`, `puan_turu: str` (örn: SAY, EA), `alt_bs: int`, `ust_bs: int` vb. (Detaylar için `yokatlas_mcp_server.py` script'indeki tool tanımına bakınız.)

4.  **`search_associate_degree_programs`**
    * **Açıklama:** Çeşitli kriterlere göre önlisans programlarını (Önlisans Tercih Sihirbazı) arar.
    * **Parametreler:** `uni_adi: str`, `program_adi: str`, `alt_puan: float`, `ust_puan: float` vb. (Detaylar için `yokatlas_mcp_server.py` script'indeki tool tanımına bakınız.)

## 🔧 Diğer MCP İstemcileri ile Kullanım

Bu bölüm, YOKATLAS MCP aracını 5ire gibi Claude Desktop dışındaki MCP istemcileriyle kullanmak isteyenler içindir.

### Ön Gereksinimler

1. **Python Kurulumu:** Sisteminizde Python 3.12 veya üzeri kurulu olmalıdır. Kurulum sırasında "Add Python to PATH" (Python'ı PATH'e ekle) seçeneğini işaretlemeyi unutmayın. [Buradan indirebilirsiniz](https://www.python.org/downloads/).

2. **Git Kurulumu (Windows):** Bilgisayarınıza git yazılımını [indirip kurun](https://git-scm.com/download/win). "Git for Windows/x64 Setup" seçeneğini indirmelisiniz.

3. **uv Kurulumu:**
   - **Windows Kullanıcıları (PowerShell):** Bir CMD ekranı açın ve bu kodu çalıştırın:
     ```bash
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```
   - **Mac/Linux Kullanıcıları (Terminal):** Bir Terminal ekranı açın ve bu kodu çalıştırın:
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```

4. **Microsoft Visual C++ Redistributable (Windows):** Bazı Python paketlerinin doğru çalışması için gereklidir. [Buradan indirip kurun](https://aka.ms/vs/17/release/vc_redist.x64.exe).

### 5ire ile Kurulum

1. İşletim sisteminize uygun 5ire MCP istemcisini indirip kurun.

2. 5ire'ı açın. **Workspace → Providers** menüsünden kullanmak istediğiniz LLM servisinin API anahtarını girin.

3. **Tools** menüsüne girin. **+Local** veya **New** yazan butona basın.

4. Aşağıdaki bilgileri girin:
   - **Tool Key:** `yokatlasmcp`
   - **Name:** `YOKATLAS MCP`
   - **Command:**
     ```
     uvx --from git+https://github.com/saidsurucu/yokatlas-mcp yokatlas-mcp
     ```

5. **Save** butonuna basarak kaydedin.

6. Şimdi **Tools** altında **YOKATLAS MCP**'yi görüyor olmalısınız. Üstüne geldiğinizde sağda çıkan butona tıklayıp etkinleştirin (yeşil ışık yanmalı).

7. Artık YOKATLAS MCP ile konuşabilirsiniz. Örnek sorgular:
   - "Boğaziçi Üniversitesi Bilgisayar Mühendisliği programının detaylarını getir"
   - "SAY puan türünde 400-500 bin sıralama aralığındaki programları ara"
   - "İstanbul'daki devlet üniversitelerinin tıp programlarını listele"

## 📜 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.