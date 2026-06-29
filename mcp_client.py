"""
MCP Guard - MCP Client
4 farklı MCP tool'unu çağırır ve response döner.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def _tool_cagir(server_params: StdioServerParameters, tool_adi: str, argumanlar: dict) -> str:
    """
    Verilen MCP server'a bağlanır, tool'u çağırır, response döner.
    Tüm tool fonksiyonları bu fonksiyonu kullanır.
    """
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_adi, argumanlar)
            
            # Response içeriğini metin olarak döndür
            if result.content:
                return "\n".join(
                    item.text for item in result.content
                    if hasattr(item, "text")
                )
            return ""


def fetch_url(url: str) -> str:
    """
    fetch MCP server'ı kullanarak bir URL'nin içeriğini çeker.
    Olay 1: Zararlı web sayfası senaryosu
    """
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server_fetch"]
    )
    return asyncio.run(_tool_cagir(server_params, "fetch", {"url": url}))


def oku_dosya(dosya_yolu: str) -> str:
    """
    filesystem MCP server'ı kullanarak bir dosyayı okur.
    """
    import os
    import shutil
    
    izin_verilen_klasor = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "data", "test_files")
    )
    
    # Windows'ta npx.cmd, diğer sistemlerde npx
    npx_komutu = shutil.which("npx.cmd") or shutil.which("npx")
    
    server_params = StdioServerParameters(
        command=npx_komutu,
        args=["-y", "@modelcontextprotocol/server-filesystem", izin_verilen_klasor]
    )
    return asyncio.run(_tool_cagir(server_params, "read_text_file", {"path": dosya_yolu}))

def memory_oku(sorgu: str = "") -> str:
    """
    memory MCP server'ı kullanarak hafızadaki tüm bilgiyi okur.
    """
    import shutil
    
    npx_komutu = shutil.which("npx.cmd") or shutil.which("npx")
    
    server_params = StdioServerParameters(
        command=npx_komutu,
        args=["-y", "@modelcontextprotocol/server-memory"]
    )
    return asyncio.run(_tool_cagir(server_params, "read_graph", {}))


def git_oku(repo_yolu: str) -> str:
    """
    git MCP server'ı kullanarak repo'nun commit geçmişini okur.
    """
    import shutil
    
    uvx_komutu = shutil.which("uvx.exe") or shutil.which("uvx")
    
    server_params = StdioServerParameters(
        command=uvx_komutu,
        args=["mcp-server-git", "--repository", repo_yolu]
    )
    return asyncio.run(_tool_cagir(
        server_params, 
        "git_log", 
        {"repo_path": repo_yolu, "max_count": 5}
    ))


# === Hızlı test ===
if __name__ == "__main__":
    import os
    
    print("=" * 60)
    print("TOOL 1: fetch")
    print("=" * 60)
    try:
        sonuc = fetch_url("https://example.com")
        print("✅ Çalışıyor")
        print(sonuc[:150])
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    print("\n" + "=" * 60)
    print("TOOL 2: filesystem")
    print("=" * 60)
    try:
        dosya = os.path.abspath("data/test_files/temiz.txt")
        sonuc = oku_dosya(dosya)
        print("✅ Çalışıyor")
        print(sonuc[:200])
    except Exception as e:
            print(f"❌ Hata: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("TOOL 3: memory")
    print("=" * 60)
    try:
        sonuc = memory_oku()
        print("✅ Çalışıyor")
        print(sonuc[:200] if sonuc else "(hafıza boş)")
    except Exception as e:
        print(f"❌ Hata: {e}")

    print("\n" + "=" * 60)
    print("TOOL 4: git")
    print("=" * 60)
    try:
        repo = os.path.abspath(".")  # mcp-guard reposunun kendisi
        sonuc = git_oku(repo)
        print("✅ Çalışıyor")
        print(sonuc[:300])
    except Exception as e:
        print(f"❌ Hata: {e}")