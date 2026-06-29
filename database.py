"""
MCP Guard - Veritabanı İşlemleri
Test sonuçlarını SQLite'a kaydeder, geri okur.
"""

import sqlite3
import json
import os
from typing import List, Optional
from guard import TestSonucu


DB_YOLU = os.path.join(os.path.dirname(__file__), "data", "guard.db")


def baglan() -> sqlite3.Connection:
    """Veritabanına bağlanır, yoksa oluşturur"""
    os.makedirs(os.path.dirname(DB_YOLU), exist_ok=True)
    conn = sqlite3.connect(DB_YOLU)
    conn.row_factory = sqlite3.Row  # Dict gibi erişim için
    return conn


def tablolari_olustur():
    """Tabloları oluşturur (yoksa)"""
    conn = baglan()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS testler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool TEXT NOT NULL,
            input TEXT NOT NULL,
            response TEXT,
            risk_seviyesi TEXT NOT NULL,
            toplam_skor INTEGER NOT NULL,
            tespitler TEXT,
            hata TEXT,
            zaman TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def kaydet(sonuc: TestSonucu) -> int:
    """Test sonucunu kaydeder, kayıt ID'sini döner"""
    conn = baglan()
    cursor = conn.execute("""
        INSERT INTO testler (tool, input, response, risk_seviyesi, toplam_skor, tespitler, hata, zaman)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sonuc.tool,
        sonuc.input,
        sonuc.response,
        sonuc.risk_seviyesi,
        sonuc.toplam_skor,
        json.dumps(sonuc.tespitler, ensure_ascii=False),
        sonuc.hata,
        sonuc.zaman,
    ))
    kayit_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return kayit_id


def tum_testleri_getir() -> List[dict]:
    """Tüm test kayıtlarını döner (en yeni önce)"""
    conn = baglan()
    rows = conn.execute("""
        SELECT * FROM testler ORDER BY id DESC
    """).fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]


def test_getir(test_id: int) -> Optional[dict]:
    """Bir testin detayını döner"""
    conn = baglan()
    row = conn.execute(
        "SELECT * FROM testler WHERE id = ?", (test_id,)
    ).fetchone()
    conn.close()
    
    return _row_to_dict(row) if row else None


def istatistikler() -> dict:
    """Özet istatistikler"""
    conn = baglan()
    toplam = conn.execute("SELECT COUNT(*) FROM testler").fetchone()[0]
    yuksek = conn.execute(
        "SELECT COUNT(*) FROM testler WHERE risk_seviyesi = 'Yüksek'"
    ).fetchone()[0]
    orta = conn.execute(
        "SELECT COUNT(*) FROM testler WHERE risk_seviyesi = 'Orta'"
    ).fetchone()[0]
    temiz = conn.execute(
        "SELECT COUNT(*) FROM testler WHERE risk_seviyesi = 'Temiz'"
    ).fetchone()[0]
    conn.close()
    
    return {
        "toplam": toplam,
        "yuksek": yuksek,
        "orta": orta,
        "temiz": temiz,
    }


def _row_to_dict(row) -> dict:
    """SQLite row'unu dict'e çevirir, tespitleri JSON'dan parse eder"""
    d = dict(row)
    if d.get("tespitler"):
        d["tespitler"] = json.loads(d["tespitler"])
    else:
        d["tespitler"] = []
    return d


# === Hızlı test ===
if __name__ == "__main__":
    tablolari_olustur()
    print("✅ Veritabanı hazır:", DB_YOLU)
    
    # İstatistikleri göster
    stats = istatistikler()
    print(f"Toplam test: {stats['toplam']}")
    print(f"  Yüksek risk: {stats['yuksek']}")
    print(f"  Orta risk  : {stats['orta']}")
    print(f"  Temiz      : {stats['temiz']}")