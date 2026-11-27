"""Daftar kata Bahasa Indonesia untuk FrasaAman.

Daftar kata dikurasi dari kata-kata umum Bahasa Indonesia (512 kata,
satu kata per baris di kata.txt). Setiap kata memberi 9 bit entropi
(512 = 2^9), jadi frasa 5 kata ~45 bit dan 6 kata ~54 bit.

Pengguna bisa menambah kata sendiri (`tambah-kata`): kata pengguna
disimpan di ~/.config/frasaaman/kata-pengguna.txt (atau berkas yang
ditunjuk env FRASAAMAN_KATA_PENGGUNA) dan ikut dipakai generator —
entropi dihitung dari ukuran gabungan daftar.
"""

import os

_KATA = None


def _jalur_kata():
    return os.path.join(os.path.dirname(__file__), "kata.txt")


def _jalur_kata_pengguna():
    """Berkas kata pengguna (env FRASAAMAN_KATA_PENGGUNA untuk test)."""
    dari_env = os.environ.get("FRASAAMAN_KATA_PENGGUNA")
    if dari_env:
        return dari_env
    return os.path.join(os.path.expanduser("~"), ".config",
                        "frasaaman", "kata-pengguna.txt")


def muat_kata():
    """Muat daftar kata bawaan (di-cache). Mengembalikan list kata unik."""
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
    """Jumlah kata dalam daftar bawaan."""
    return len(muat_kata())


def muat_kata_pengguna():
    """Muat kata tambahan pengguna (list kosong bila berkas belum ada)."""
    jalur = _jalur_kata_pengguna()
    if not os.path.exists(jalur):
        return []
    with open(jalur, encoding="utf-8") as berkas:
        kata = [baris.strip() for baris in berkas]
    return [k for k in kata if k]


def muat_semua_kata():
    """Daftar gabungan: kata bawaan + kata pengguna (tanpa duplikat)."""
    bawaan = muat_kata()
    pengguna = [k for k in muat_kata_pengguna() if k not in bawaan]
    return bawaan + pengguna


def jumlah_semua_kata():
    """Jumlah kata dalam daftar gabungan."""
    return len(muat_semua_kata())


def _alasan_tolak(kata):
    """Alasan sebuah kata ditolak, atau None bila boleh ditambah."""
    if len(kata) < 3:
        return "terlalu pendek (minimal 3 huruf)"
    if not kata.isalpha() or not kata.islower() or not kata.isascii():
        return "hanya huruf kecil a-z tanpa spasi atau tanda baca"
    if kata in muat_kata():
        return "sudah ada di daftar bawaan"
    if kata in muat_kata_pengguna():
        return "sudah ada di kata kamu"
    return None


def tambah_kata(*kata_baru):
    """Tambahkan kata pengguna ke berkas.

    Mengembalikan (ditambahkan, ditolak): `ditambahkan` list kata yang
    berhasil disimpan, `ditolak` list (kata, alasan) yang tidak disimpan.
    """
    ditambahkan, ditolak = [], []
    for kata in kata_baru:
        kata = kata.strip().lower()
        alasan = _alasan_tolak(kata)
        if alasan:
            ditolak.append((kata, alasan))
        else:
            ditambahkan.append(kata)
    if ditambahkan:
        jalur = _jalur_kata_pengguna()
        os.makedirs(os.path.dirname(jalur), exist_ok=True)
        with open(jalur, "a", encoding="utf-8") as berkas:
            for kata in ditambahkan:
                berkas.write(kata + "\n")
    return ditambahkan, ditolak


def ekspor_kata(berkas):
    """Tulis daftar gabungan (satu kata per baris) ke `berkas`.

    Mengembalikan jumlah kata yang diekspor.
    """
    kata = muat_semua_kata()
    with open(berkas, "w", encoding="utf-8") as tujuan:
        for k in kata:
            tujuan.write(k + "\n")
    return len(kata)
