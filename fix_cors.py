from pathlib import Path

p = Path("backend/main.py")
s = p.read_text(encoding="utf-8-sig")

if "from fastapi.middleware.cors import CORSMiddleware" not in s:
    s = s.replace(
        "from fastapi import FastAPI",
        "from fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware"
    )

if "app.add_middleware(CORSMiddleware" not in s:
    marker = "app = FastAPI("
    start = s.find(marker)

    if start != -1:
        line_end = s.find("\n", start)

        middleware = '''

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''

        s = s[:line_end + 1] + middleware + s[line_end + 1:]

p.write_text(s, encoding="utf-8")
print("CORS configuration added.")
