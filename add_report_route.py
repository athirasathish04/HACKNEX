from pathlib import Path

path = Path("backend/main.py")
text = path.read_text(encoding="utf-8-sig")

# Add the import after the robustness import
robustness_import = "from backend.routes.robustness import router as robustness_router"
report_import = "from backend.routes.report import router as report_router"

if report_import not in text:
    text = text.replace(
        robustness_import,
        robustness_import + "\n" + report_import
    )

# Add the router after robustness_router
robustness_block = '''app.include_router(
    robustness_router,
    prefix="/api"
)'''

report_block = '''app.include_router(
    report_router,
    prefix="/api"
)'''

if "app.include_router(\n    report_router" not in text:
    text = text.replace(
        robustness_block,
        robustness_block + "\n\n" + report_block
    )

path.write_text(text, encoding="utf-8")

print("Report router added successfully.")
