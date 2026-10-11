from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Our Arcade",
    description="A shared arcade for games and puzzles.",
    version="0.1.0",
)


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Our Arcade</title>
        </head>
        <body>
            <h1>Our Arcade</h1>
            <p>System online.</p>
        </body>
    </html>
    """


@app.get("/health")
async def health():
    return {"status": "ok"}
