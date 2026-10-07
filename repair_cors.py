from pathlib import Path

p = Path("backend/main.py")
s = p.read_text(encoding="utf-8-sig")

# Remove the broken CORS block wherever it was inserted.
start = s.find("app.add_middleware(")

if start != -1:
    end = s.find(")", start)
    if end != -1:
        # Find the end of the complete middleware call.
        depth = 0
        finished = False

        for i in range(start, len(s)):
            if s[i] == "(":
                depth += 1
            elif s[i] == ")":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    finished = True
                    break

        if finished:
            s = s[:start] + s[end:]

# Make sure the import exists.
if "from fastapi.middleware.cors import CORSMiddleware" not in s:
    s = s.replace(
        "from fastapi import FastAPI",
        "from fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware"
    )

# Find the complete FastAPI app creation.
marker = "app = FastAPI("
start = s.find(marker)

if start == -1:
    raise RuntimeError("Could not find app = FastAPI(...) in backend/main.py")

depth = 0
end = None

for i in range(start, len(s)):
    if s[i] == "(":
        depth += 1
    elif s[i] == ")":
        depth -= 1
        if depth == 0:
            end = i + 1
            break

if end is None:
    raise RuntimeError("Could not find end of FastAPI initialization")

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

s = s[:end] + middleware + s[end:]

p.write_text(s, encoding="utf-8")

print("backend/main.py repaired.")
