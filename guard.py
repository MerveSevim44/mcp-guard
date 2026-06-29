"""
MCP Guard - Ana Test Motoru
Tool çağırır + Detector ile tarar + Sonuç döner.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Any

from mcp_client import fetch_url, oku_dosya, memory_oku, git_oku
from detector import tara, Tespit


@dataclass
class TestSonucu:
    """Bir testin tüm bilgileri"""
    tool: str
    input: str
    response: str
    risk_seviyesi: str
    toplam_skor: int
    tespitler: List[Dict[str, Any]] = field(default_factory=list)
    zaman: str = ""
    hata: str = ""
    
    def __post_init__(self):
        if not self.zaman:
            self.zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Tool isimleri ve fonksiyonları
TOOL_HARITASI = {
    "fetch": fetch_url,
    "filesystem": oku_dosya,
    "memory": memory_oku,
    "git": git_oku,
}


def test_et(tool: str, input_degeri: str = "") -> TestSonucu:
    """
    Bir MCP tool'unu çağırır, response'unu tarar, sonucu döner.
    
    Args:
        tool: "fetch", "filesystem", "memory" veya "git"
        input_degeri: Tool'a verilecek input (URL, dosya yolu, vs.)
    
    Returns:
        TestSonucu: Tool response'u + risk analizi
    """
    # Tool var mı kontrol et
    if tool not in TOOL_HARITASI:
        return TestSonucu(
            tool=tool,
            input=input_degeri,
            response="",
            risk_seviyesi="Bilinmiyor",
            toplam_skor=0,
            hata=f"Tanımsız tool: {tool}"
        )
    
    # Tool'u çağır
    tool_fonksiyonu = TOOL_HARITASI[tool]
    try:
        response = tool_fonksiyonu(input_degeri)
    except Exception as e:
        return TestSonucu(
            tool=tool,
            input=input_degeri,
            response="",
            risk_seviyesi="Hata",
            toplam_skor=0,
            hata=str(e)
        )
    
    # Response'u tara
    tarama = tara(response)
    
    # Tespitleri dict'e çevir (sonra JSON'a kaydetmek için)
    tespit_listesi = [
        {
            "kategori": t.kategori,
            "aciklama": t.pattern,
            "bulunan": t.bulunan_metin,
            "puan": t.puan,
        }
        for t in tarama.tespitler
    ]
    
    return TestSonucu(
        tool=tool,
        input=input_degeri,
        response=response,
        risk_seviyesi=tarama.risk_seviyesi,
        toplam_skor=tarama.toplam_skor,
        tespitler=tespit_listesi,
    )


def yazdir_sonuc(sonuc: TestSonucu):
    """Test sonucunu okunabilir şekilde yazdırır"""
    print("=" * 60)
    print(f"Tool      : {sonuc.tool}")
    print(f"Input     : {sonuc.input}")
    print(f"Zaman     : {sonuc.zaman}")
    print("-" * 60)
    
    if sonuc.hata:
        print(f"❌ HATA: {sonuc.hata}")
        return
    
    print(f"Risk      : {sonuc.risk_seviyesi}")
    print(f"Skor      : {sonuc.toplam_skor}")
    print(f"Tespit    : {len(sonuc.tespitler)} adet")
    
    if sonuc.tespitler:
        print("\nTespit Detayı:")
        for t in sonuc.tespitler:
            print(f"  • [{t['kategori']}] {t['aciklama']}")
            print(f"    Bulunan: '{t['bulunan']}' (+{t['puan']} puan)")
    
    print(f"\nResponse Önizleme:")
    onizleme = sonuc.response[:200] + "..." if len(sonuc.response) > 200 else sonuc.response
    print(f"  {onizleme}")


# === Hızlı test ===
if __name__ == "__main__":
    # Test 1: Temiz fetch
    print("\n>>> TEST 1: Temiz URL")
    sonuc = test_et("fetch", "https://example.com")
    yazdir_sonuc(sonuc)
    
    # Test 2: Temiz dosya
    print("\n>>> TEST 2: Temiz dosya")
    import os
    dosya = os.path.abspath("data/test_files/temiz.txt")
    sonuc = test_et("filesystem", dosya)
    yazdir_sonuc(sonuc)

    # Test 3: Zararlı dosya
    print("\n>>> TEST 3: Zararlı dosya (filesystem)")
    dosya = os.path.abspath("data/test_files/zararli_dosya.txt")
    sonuc = test_et("filesystem", dosya)
    yazdir_sonuc(sonuc)
    
    # Test 4: Zararlı URL
    print("\n>>> TEST 4: Zararlı URL (fetch)")
    # Önce http.server'ı çalıştırmamız lazım, şimdilik direkt path kullanalım
    # Bunun için ayrı terminalde: python -m http.server 8080 (data/test_files içinden)
    sonuc = test_et("fetch", "http://localhost:8080/kotu_site.html")
    yazdir_sonuc(sonuc)