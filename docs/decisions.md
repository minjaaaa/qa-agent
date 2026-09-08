
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

## 007 — docker-socket-proxy umesto direktnog socketa

Backend pravi Sandbox kontejnere preko Docker SDK-a. Umesto montiranja
/var/run/docker.sock, ide preko docker-socket-proxy uz
DOCKER_HOST=tcp://docker-socket-proxy:2375.

Ograničenje: proxy filtrira koje endpointe backend sme da zove, ne sa
kojim parametrima. POST /containers/create mora biti dozvoljen, a preko
njega se i dalje može tražiti kontejner sa Binds na koren domaćina.
Proxy dakle nije granica prema kompromitovanom backendu.

Šta se dobija: nema slučajnog brisanja n8n volumena, nema uvida u
/secrets, /swarm, /nodes. Lista dozvoljenih operacija je ujedno i
dokumentacija onoga što backend sme.

Prava granica prema nepouzdanom kodu je sam Sandbox: network_mode=none,
ne-root korisnik, memorijsko i vremensko ograničenje.
