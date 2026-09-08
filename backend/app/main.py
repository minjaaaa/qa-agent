import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.modeli import OdgovorSaTestovima, ZahtevZaTestove
from app.podesavanja import podesavanja

from fastapi.exceptions import RequestValidationError

logging.basicConfig(
    level=podesavanja.log_nivo,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger("qa-backend")

app = FastAPI(title="QA Agent Backend", version="0.1.0")


@app.middleware("http")
async def prati_zahtev(request: Request, call_next):
    oznaka = uuid.uuid4().hex[:8]
    pocetak = time.monotonic()
    log.info("[%s] --> %s %s", oznaka, request.method, request.url.path)
    odgovor = await call_next(request)
    trajanje = (time.monotonic() - pocetak) * 1000
    log.info(
        "[%s] <-- %s za %.0f ms", oznaka, odgovor.status_code, trajanje
    )
    odgovor.headers["X-Oznaka-Zahteva"] = oznaka
    return odgovor


@app.get("/health")
def health():
    return {"status": "ok", "verzija": app.version}


@app.post("/generate-tests", response_model=OdgovorSaTestovima)
def generisi_testove(zahtev: ZahtevZaTestove) -> OdgovorSaTestovima:
    log.info(
        "Zahtev: repo=%s grana=%s sha=%s fajlova=%d diff=%d B",
        zahtev.repo,
        zahtev.grana,
        zahtev.commit_sha[:7],
        len(zahtev.izmenjeni_fajlovi),
        len(zahtev.diff),
    )
    return OdgovorSaTestovima(
        status="ok",
        generisani_testovi=[],
        broj_pokusaja=0,
        poruka=(
            f"Backend je primio {len(zahtev.izmenjeni_fajlovi)} fajl(ova). "
            "Generator testova još nije implementiran (D4)."
        ),
    )



@app.exception_handler(RequestValidationError)
async def neispravan_zahtev(request: Request, exc: RequestValidationError):
    log.warning("Zahtev ne odgovara ugovoru: %s", exc.errors())
    return JSONResponse(
        status_code=422,
        content=OdgovorSaTestovima(
            status="greska",
            poruka="Zahtev ne odgovara ugovoru verzije 1.",
        ).model_dump(by_alias=True),
    )


@app.exception_handler(Exception)
async def neocekivana_greska(request: Request, exc: Exception):
    log.exception("Neočekivana greška")
    return JSONResponse(
        status_code=500,
        content=OdgovorSaTestovima(
            status="greska",
            poruka="Interna greška backenda.",
        ).model_dump(by_alias=True),
    )