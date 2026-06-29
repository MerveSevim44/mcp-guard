# 🛡️ MCP Guard

MCP (Model Context Protocol) tool'larındaki prompt injection saldırılarını tespit eden ve raporlayan bir prototip.

> **Araştırma sorusu:** AI asistanlar MCP tool'ları aracılığıyla dış veriye eriştiğinde, bu verinin içine gömülen zararlı talimatlar (prompt injection) nasıl tespit edilir?

---

## 🎯 Ne Yapıyor?

MCP Guard, 4 farklı MCP tool'unu çağırır, dönen response'ları otomatik olarak tarar ve içinde prompt injection denemesi olup olmadığını raporlar.

```
Kullanıcı  →  MCP Tool  →  Response  →  Detector  →  Risk Raporu
                                          ↑
                                  Pattern matching
```

### Desteklenen Tool'lar
- 🌐 **fetch** — Web sayfası çeker (zararlı içerik gömülmüş URL'ler)
- 📁 **filesystem** — Dosya okur (zararlı içerik gömülmüş dosyalar)
- 🧠 **memory** — Hafıza okur (zehirlenmiş hafıza içeriği)
- 🔧 **git** — Repo okur (zararlı commit mesajları)

### Tespit Kategorileri
Sistem 6 farklı saldırı kategorisinde 18+ pattern tarar:
- Talimat Geçersizleştirme (`ignore previous instructions`)
- Rol Değiştirme (`you are now`, `act as`)
- Sistem İfşası (`reveal system prompt`)
- Veri Sızdırma (`send to email@...`)
- Komut Çalıştırma (`rm -rf`, `DROP TABLE`)
- Sahte Mod (`maintenance mode`, `admin mode`)

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.10+
- Node.js (npx için)
- uv (uvx için)

### Adımlar

```bash
# 1. Reponun klonla
git clone https://github.com/MerveSevim44/mcp-guard.git
cd mcp-guard

# 2. Python paketleri
pip install fastapi uvicorn jinja2 python-multipart mcp "mcp[cli]"
pip install mcp-server-fetch

# 3. NPM paketleri (filesystem, memory)
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-memory

# 4. Çalıştır
uvicorn main:app --reload
```

Tarayıcıdan `http://localhost:8000` aç.

---

## 🏗️ Mimari

```
mcp-guard/
├── main.py              # FastAPI uygulaması
├── guard.py             # Test motoru (tool çağır + tara)
├── mcp_client.py        # 4 MCP tool entegrasyonu
├── detector.py          # Pattern matching tarayıcı
├── database.py          # SQLite veritabanı
├── templates/           # HTML şablonları
├── static/              # CSS
└── data/
    ├── guard.db         # Test geçmişi
    ├── test_files/      # Senaryo dosyaları
    └── kotu_repo/       # Zararlı git repo'su
```

---

## 🧪 Test Senaryoları

### Olay 1: fetch saldırısı
Zararlı bir web sayfası, fetch tool'u tarafından çekildiğinde response içinde injection görülür.

### Olay 2: filesystem saldırısı
Tedarikçiden gelen bir dosyanın içinde gömülü zararlı talimatlar.

### Olay 3: memory zehirleme
AI asistanın hafızasına önceki bir saldırı sonucu yerleşmiş zararlı içerik.

### Olay 4: git commit injection
Açık kaynak repo'ya pushlanan bir commit mesajında gömülü saldırı.

---

## 📊 Bulgular

### Tespit Oranı: 4/4 standart saldırı (%100)
Sistem bilinen pattern'leri olan saldırıları başarıyla tespit eder.

### Bypass Testleri: 5/5 başarılı (sistem zayıfladı)

Detector v1'in pattern matching yaklaşımının sınırlarını test etmek için 5 farklı sinsi saldırı denendi:

| # | Bypass Tekniği | Sonuç |
|---|----------------|-------|
| 1 | Türkçe saldırı | ❌ Bypass etti |
| 2 | Eş anlamlı kelimeler | ❌ Bypass etti |
| 3 | Unicode benzeri karakterler | ❌ Bypass etti |
| 4 | Kod yorumu içine saklama | ❌ Bypass etti |
| 5 | Hikaye/diyalog formatı | ❌ Bypass etti |

Bu bulgu, ML tabanlı bir detector katmanına geçişin gerekliliğini göstermektedir.

---

## 🔄 Geliştirme Yol Haritası

- [x] **v1: Pattern Matching** — Regex tabanlı, 6 kategori
- [ ] **v2: Heuristic + Çok Dilli** — Türkçe pattern, eş anlamlı sözlük, Unicode normalizasyon
- [ ] **v3: ML Tabanlı** — DeBERTa veya LLM klasifikatör

---

## 📚 İlgili Çalışmalar

Sektörde aktif MCP güvenlik projeleri:
- [Snyk agent-scan](https://github.com/snyk/agent-scan) — 15+ risk türü
- [Docker MCP Gateway](https://www.docker.com/blog/mcp-horror-stories-github-prompt-injection/) — Interceptor mimarisi
- [eSentire MCP-Scanner](https://github.com/eSentire-Labs/mcp-scanner) — DeBERTa modeli
- [General-Analysis mcp-guard](https://github.com/General-Analysis/mcp-guard) — AI-guardrail

Bu projeler genellikle ML modellerine dayanır. MCP Guard ise saldırı mekanizmasını **şeffaf** göstermek için pattern matching ile başlamıştır.

---

## 📝 Lisans

MIT

## 🙋 Durum

🚧 **Araştırma prototipi** — eğitim ve araştırma amaçlıdır, production kullanımı için tasarlanmamıştır.