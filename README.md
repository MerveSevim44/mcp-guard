# 🛡️ MCP Guard

MCP (Model Context Protocol) tool'larındaki prompt injection saldırılarını tespit eden ve raporlayan bir prototip.

## Özellikler
- 4 farklı MCP tool desteği: fetch, filesystem, memory, git
- Otomatik prompt injection tespiti
- Risk skorlama
- Test geçmişi ve raporlama dashboard'u


## İlgili Çalışmalar

Bu konuda sektörde aktif çalışmalar var:

1. General-Analysis/mcp-guard — AI-tabanlı moderation
2. Snyk agent-scan — 15+ risk türü için scanner  
3. MCP-Scanner (eSentire) — DeBERTa ML modeli ile detection
4. Docker MCP Gateway — Tool call interceptor mimarisi

Bu çalışmalar genellikle ML modellerine veya proxy mimarilerine dayanıyor.
Bu prototipte ise pattern matching ile başlanmıştır — amaç saldırı 
mekanizmasını şeffaf şekilde göstermektir.

## Kurulum
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Durum
🚧 Geliştirme aşamasında