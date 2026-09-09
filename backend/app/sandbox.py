import logging
import tarfile
import io

import docker
from docker.errors import DockerException, ImageNotFound

log = logging.getLogger("qa-backend.sandbox")

SLIKA = "qa-sandbox:latest"
MEM_LIMIT = "256m"
VREME_S = 60


class RezultatIzvrsavanja:
    def __init__(self, uspeh: bool, izlazni_kod: int, izlaz: str, razlog: str = ""):
        self.uspeh = uspeh
        self.izlazni_kod = izlazni_kod
        self.izlaz = izlaz
        self.razlog = razlog

    def __repr__(self):
        return (
            f"<Rezultat uspeh={self.uspeh} kod={self.izlazni_kod} "
            f"razlog={self.razlog!r}>"
        )


def _arhiva(fajlovi: dict[str, str]) -> io.BytesIO:
    """Pravi tar arhivu u memoriji, za put_archive."""
    bafer = io.BytesIO()
    with tarfile.open(fileobj=bafer, mode="w") as tar:
        for putanja, sadrzaj in fajlovi.items():
            podaci = sadrzaj.encode("utf-8")
            info = tarfile.TarInfo(name=putanja)
            info.size = len(podaci)
            info.mode = 0o644
            tar.addfile(info, io.BytesIO(podaci))
    bafer.seek(0)
    return bafer

def izvrsi_testove(fajlovi: dict[str, str]) -> RezultatIzvrsavanja:
    """Pokreće pytest nad datim fajlovima u prolaznom kontejneru."""
    try:
        klijent = docker.from_env()
    except DockerException as e:
        log.error("Nema veze sa Docker demonom: %s", e)
        return RezultatIzvrsavanja(False, -1, "", "nema-dokera")

    kontejner = None
    try:
        kontejner = klijent.containers.create(
            SLIKA,
            command=["pytest", "-v", "--tb=short"],
            network_mode="none",
            mem_limit=MEM_LIMIT,
            working_dir="/rad",
            environment={"PYTHONPATH": "/rad"},
        )
        kontejner.put_archive("/rad", _arhiva(fajlovi))
        kontejner.start()

        try:
            ishod = kontejner.wait(timeout=VREME_S)
            kod = ishod.get("StatusCode", -1)
        except Exception:
            log.warning("Isteklo vreme od %d s, ubijam kontejner", VREME_S)
            kontejner.kill()
            izlaz = kontejner.logs().decode("utf-8", errors="replace")
            return RezultatIzvrsavanja(False, -1, izlaz, "isteklo-vreme")

        izlaz = kontejner.logs().decode("utf-8", errors="replace")

        if kod == 137:
            return RezultatIzvrsavanja(False, kod, izlaz, "nema-memorije")

        return RezultatIzvrsavanja(kod == 0, kod, izlaz)

    except ImageNotFound:
        log.error("Slika %s ne postoji", SLIKA)
        return RezultatIzvrsavanja(False, -1, "", "nema-slike")
    except DockerException as e:
        log.exception("Greška u sandbox-u")
        return RezultatIzvrsavanja(False, -1, str(e), "greska-dokera")
    finally: # uvijek brisem kontejner
        if kontejner is not None:
            try:
                kontejner.remove(force=True)
            except DockerException:
                log.warning("Nisam uspela da obrišem kontejner")