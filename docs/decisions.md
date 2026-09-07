
## 004 — Raw Body na Webhook node-u
Opcija je ukljucena zaobilaznim putem, prebacivanjem Respond rezima.
Ako se pri izmeni node-a izgubi, provera potpisa prelazi na rezervni
put koji ponovo sklapa JSON i moze tiho da pocne da pada.

## 005 — Slack preko bot tokena, ne webhook URL-a
Bot API trazi scope chat:write i popunjen Notification Text uz Blocks.
Token zivi u n8n credentialu, ne u .env, pa ne curi kroz eksport.

## Rizici za Nedelju 2

- docker.sock: backend treba da pravi Sandbox kontejnere. Montiranje
  socketa u kontejner daje mu prava root korisnika na domacinu.
  Razmotriti alternative pre implementacije.
- Sandbox mora imati iskljucenu mrezu i vremensko ogranicenje.
- URL u node-u `Pozovi backend` menja se sa
  http://localhost:5678/webhook/generate-tests
  na http://qa-backend:8000/generate-tests
- Backend nema mapiran port, dostupan je samo iz qa-net mreze.
- Putanja endpointa je /generate-tests, sa slovom s na kraju.
