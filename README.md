# QA Agent — infrastruktura

Autonomni QA agent koji na push u repozitorijum generise pytest testove,
izvrsava ih u izolovanom Docker kontejneru i otvara Pull Request.

## Pokretanje

1. Kopiraj `.env.example` u `.env` i popuni vrednosti
2. `docker compose up -d`
3. Editor: http://localhost:5678

## Servisi

- `n8n` — orkestracija, port 5678
- `ngrok` — tunel za GitHub webhook-ove

## Workflow-i

- `01-github-push` — glavni tok
- `02-mock-backend` — privremena zamena za Python backend
- `99-greske` — obavestenja o padovima

Credentials se ne eksportuju. Posle uvoza workflow-a treba
ponovo uneti GitHub i Slack pristupne podatke.

## Dokumentacija

- `docs/api-contract.md` — ugovor n8n prema backendu
- `docs/decisions.md` — inzenjerske odluke
