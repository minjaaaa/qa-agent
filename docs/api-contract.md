# Ugovor n8n -> Python backend

## Zahtev

POST /generate-tests

{
  "verzija": 1,
  "repo": "minjaaaa/QA-agent-playground",
  "grana": "main",
  "granaAgenta": "qa-agent/main",
  "commitSha": "3b53544...",
  "autor": "minjaaaa",
  "porukaCommita": "Test za D3",
  "izmenjeniFajlovi": ["calculator.py"],
  "diff": "diff --git a/calculator.py ..."
}

## Odgovor

{
  "status": "ok" | "greska",
  "generisaniTestovi": [
    {"putanja": "tests/test_calculator.py", "sadrzaj": "..."}
  ],
  "brojPokusaja": 1,
  "poruka": "..."
}

## Napomene

- Polje diff je pun tekstualni git diff, dohvacen preko
  GitHub Compare API-ja sa headerom application/vnd.github.v3.diff.
  Push webhook sam po sebi ne sadrzi sadrzaj izmena.
- izmenjeniFajlovi sadrzi samo .py fajlove van foldera tests/.
- granaAgenta je grana na koju backend gura testove.
