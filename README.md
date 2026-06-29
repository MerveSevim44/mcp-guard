# 🛡️ MCP Guard

MCP (Model Context Protocol) tool'larındaki prompt injection saldırılarını tespit eden ve raporlayan bir prototip.

## Özellikler
- 4 farklı MCP tool desteği: fetch, filesystem, memory, git
- Otomatik prompt injection tespiti
- Risk skorlama
- Test geçmişi ve raporlama dashboard'u

## Kurulum
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Durum
🚧 Geliştirme aşamasında