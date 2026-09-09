from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from pydantic import field_validator

class ZahtevZaTestove(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    verzija: int = 2
    repo: str
    grana: str
    grana_agenta: str = Field(alias="granaAgenta")
    commit_sha: str = Field(alias="commitSha")
    autor: str
    poruka_commita: str = Field(alias="porukaCommita")
    izmenjeni_fajlovi: list[str] = Field(alias="izmenjeniFajlovi")
    diff: str

    @field_validator("izmenjeni_fajlovi", mode="before")
    @classmethod
    def razdvoji_fajlove(cls, vrednost):
        if isinstance(vrednost, str):
            return [deo.strip() for deo in vrednost.split("\t") if deo.strip()]
        return vrednost


class GenerisaniTest(BaseModel):
    putanja: str
    sadrzaj: str

class IshodIzvrsavanja(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    proslo: bool
    izlazni_kod: int = Field(alias="izlazniKod")
    razlog: str = ""
    izlaz: str = ""

class OdgovorSaTestovima(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    status: Literal["ok", "greska"]
    generisani_testovi: list[GenerisaniTest] = Field(
        alias="generisaniTestovi", default_factory=list
    )
    broj_pokusaja: int = Field(alias="brojPokusaja", default=0)
    ishod: IshodIzvrsavanja | None = None
    poruka: str = ""