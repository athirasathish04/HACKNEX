from pathlib import Path

path = Path("backend/main.py")
text = path.read_text(encoding="utf-8-sig")

text = text.replace(
    "from backend.routes.robustness import router as robustness_router`nfrom backend.routes.report import router as report_router",
    "from backend.routes.robustness import router as robustness_router\nfrom backend.routes.report import router as report_router"
)

text = text.replace(
    'app.include_router(robustness_router, prefix="/api")`napp.include_router(report_router, prefix="/api")',
    'app.include_router(robustness_router, prefix="/api")\napp.include_router(report_router, prefix="/api")'
)

path.write_text(text, encoding="utf-8")

print("backend/main.py repaired.")
