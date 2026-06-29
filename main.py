from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="MCP Guard")


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>MCP Guard</title></head>
        <body style="font-family: sans-serif; padding: 40px;">
            <h1>🛡️ MCP Guard</h1>
            <p>MCP Prompt Injection Detector — çalışıyor!</p>
        </body>
    </html>
    """