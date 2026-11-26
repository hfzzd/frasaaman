"""Daftar kata Bahasa Indonesia untuk FrasaAman.

Daftar kata dikurasi dari kata-kata umum Bahasa Indonesia (512 kata,
satu kata per baris di kata.txt). Setiap kata memberi 9 bit entropi
(512 = 2^9), jadi frasa 5 kata ~45 bit dan 6 kata ~54 bit.
"""

import os

_KATA = None


def _jalur_kata():
    return os.path.join(os.path.dirname(__file__), "kata.txt")


def muat_kata():
    """Muat daftar kata (di-cache). Mengembalikan list kata unik."""
    global _KATA
    if _KATA is None:
        with open(_jalur_kata(), encoding="utf-8") as berkas:
            kata = [baris.strip() for baris in berkas]
        kata = [k for k in kata if k]
        if len(set(kata)) != len(kata):
            raise ValueError("daftar kata mengandung duplikat")
        _KATA = kata
    return _KATA


def jumlah_kata():
    """Jumlah kata dalam daftar."""
    return len(muat_kata())
