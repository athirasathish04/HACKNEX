from pathlib import Path

p = Path("ai/analysis/forensic_report.py")
s = p.read_text(encoding="utf-8-sig")

s = s.replace(
    "from ai.analysis.engine import analyze_input\n",
    ""
)

s = s.replace(
    "    analysis = analyze_input(str(path))",
    "    from ai.analysis.engine import analyze_input\n    analysis = analyze_input(str(path))"
)

p.write_text(s, encoding="utf-8")
print("Circular import fixed.")
