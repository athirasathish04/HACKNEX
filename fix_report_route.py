from pathlib import Path

p = Path("backend/main.py")
s = p.read_text(encoding="utf-8-sig")

if "from backend.routes.report import router as report_router" not in s:
    s = s.replace(
        "from backend.routes.robustness import router as robustness_router",
        "from backend.routes.robustness import router as robustness_router\nfrom backend.routes.report import router as report_router"
    )

if "report_router" not in s[s.find("app.include_router"):]:
    marker = '''app.include_router(
    robustness_router,
    prefix="/api"
)'''
    replacement = marker + '''

app.include_router(
    report_router,
    prefix="/api"
)'''
    s = s.replace(marker, replacement)

p.write_text(s, encoding="utf-8")
print("Report route added.")
