"""
MCP Guard - Ana Web Uygulaması
Dashboard, test çalıştırma, sonuç gösterimi.
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from guard import test_et
import database


app = FastAPI(title="MCP Guard")

# Statik dosyalar ve şablonlar
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Başlangıçta veritabanını hazırla
database.tablolari_olustur()


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "testler": database.tum_testleri_getir(),
            "stats": database.istatistikler(),
        }
    )


@app.post("/test")
def test_calistir(tool: str = Form(...), input_degeri: str = Form(...)):
    """Yeni bir test çalıştırır ve dashboard'a yönlendirir"""
    sonuc = test_et(tool, input_degeri)
    database.kaydet(sonuc)
    return RedirectResponse(url="/", status_code=303)


@app.get("/test/{test_id}", response_class=HTMLResponse)
def test_detay(request: Request, test_id: int):
    test = database.test_getir(test_id)
    if not test:
        return HTMLResponse("Test bulunamadı", status_code=404)
    return templates.TemplateResponse(
        request,
        "test_detail.html",
        {"test": test}
    )