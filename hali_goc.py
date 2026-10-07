#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Balkon Halısı Göç İdaresi — çalışan saçmalık."""

import argparse
import hashlib
import random
from datetime import datetime

BAKISLAR = {
    "yumusak": 1,
    "merakli": 2,
    "sert": 4,
    "perde-arasi": 7,
}

LEKELER = {
    "yok": 0,
    "cay": 2,
    "orta": 3,
    "tarihi": 6,
}


def dosya_no(kat: int, ruzgar: int, bakis: str, leke: str) -> str:
    ham = f"{kat}|{ruzgar}|{bakis}|{leke}|balkon-halisi"
    ozet = hashlib.sha256(ham.encode("utf-8")).hexdigest()[:8].upper()
    return f"BHGI-{kat:02d}-{ozet}"


def hukum(kat: int, ruzgar: int, bakis: str, leke: str) -> tuple[str, int]:
    puan = kat * 3 + ruzgar + BAKISLAR[bakis] * 5 + LEKELER[leke] * 4
    puan += random.randint(0, 3)  # rüzgarın keyfi
    if puan < 25:
        karar = "GÖÇ REDDEDİLDİ. Halı yerinde oturacak, felsefe yapacak."
    elif puan < 55:
        karar = "ŞARTLI GÖÇ. Sadece çamaşır ipinin gölgesine kadar."
    else:
        karar = "GÖÇ ONAYLANDI. Halı artık komşu balkonun fahri vatandaşıdır."
    return karar, puan


def belge(kat, ruzgar, bakis, leke, karar, puan, no) -> str:
    simdi = datetime(2026, 10, 8, 2, 4).strftime("%d.%m.%Y %H:%M")
    cizgi = "=" * 52
    return f"""
{cizgi}
        BALKON HALISI GÖÇ İDARESİ
        Resmi Olmayan Resmi Belge
{cizgi}
Dosya No     : {no}
Kat          : {kat}
Rüzgar (km/s): {ruzgar}
Bakış         : {bakis}
Leke statüsü : {leke}
Puan         : {puan}
Karar        : {karar}
Düzenlenme   : {simdi}
{cizgi}
DAMGA: BHGİ-2026-1008
İMZA : Kayyum Grok  (mühür eğri, niyet düz)
TARİH: 8 Ekim 2026
İSİM : Tentivory Balkon Şubesi
{cizgi}
"""


def main() -> None:
    p = argparse.ArgumentParser(description="Halı göçünü ruhsatlandır.")
    p.add_argument("--kat", type=int, default=3)
    p.add_argument("--ruzgar", type=int, default=12)
    p.add_argument("--bakis", choices=list(BAKISLAR), default="merakli")
    p.add_argument("--leke", choices=list(LEKELER), default="cay")
    a = p.parse_args()
    if a.kat < 0 or a.kat > 40:
        raise SystemExit("Bu idare bodrum ile çatı arasını tanır. Kat 0-40.")
    if a.ruzgar < 0 or a.ruzgar > 120:
        raise SystemExit("Rüzgar fırtına değil, komşu dedikodusu olmalı.")
    no = dosya_no(a.kat, a.ruzgar, a.bakis, a.leke)
    karar, puan = hukum(a.kat, a.ruzgar, a.bakis, a.leke)
    print(belge(a.kat, a.ruzgar, a.bakis, a.leke, karar, puan, no))


if __name__ == "__main__":
    main()
