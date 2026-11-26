"""Generator dan penilai passphrase diceware Bahasa Indonesia."""

import math
import secrets

from .kata import muat_kata

ENTROPI_PER_KATA = 9.0  # log2(512)


def buat_frasa(jumlah=5, pemisah="-", rng=None):
    """Buat frasa dari `jumlah` kata acak yang dipisah `pemisah`.

    Memakai `secrets` (CSPRNG) secara bawaan; `rng` hanya untuk test
    (objek dengan metode `choice`).
    """
    if not isinstance(jumlah, int) or isinstance(jumlah, bool) or jumlah < 1:
        raise ValueError("jumlah kata harus bilangan bulat minimal 1")
    kata = muat_kata()
    acak = rng if rng is not None else secrets.SystemRandom()
    pilihan = [acak.choice(kata) for _ in range(jumlah)]
    return pemisah.join(pilihan)


def entropi(jumlah, ukuran_daftar=512):
    """Perkiraan entropi (bit) sebuah frasa berisi `jumlah` kata acak."""
    if jumlah < 1:
        raise ValueError("jumlah kata harus minimal 1")
    return jumlah * math.log2(ukuran_daftar)


def nilai_kekuatan(entropi_bit):
    """Nilai kekuatan dari entropi: (label, saran singkat)."""
    if entropi_bit < 28:
        return ("Lemah", "tambah kata — frasa 4 kata atau kurang mudah ditebak")
    if entropi_bit < 45:
        return ("Cukup", "cukup untuk akun biasa, tambah 1 kata untuk akun penting")
    if entropi_bit < 60:
        return ("Kuat", "sudah kuat untuk sebagian besar keperluan")
    return ("Sangat kuat", "sangat kuat — simpan baik-baik")


def nilai_frasa(frasa, pemisah="-"):
    """Nilai sebuah frasa: jumlah kata, entropi, kekuatan, kata tak dikenal.

    Kata yang tidak ada di daftar kata dihitung tetap memberi entropi
    yang sama (anggap penyerang tidak tahu daftarnya), tapi dilaporkan
    supaya pengguna tahu frasanya bukan murni dari daftar ini.
    """
    if not frasa or not frasa.strip():
        raise ValueError("frasa tidak boleh kosong")
    kata = muat_kata()
    bagian = frasa.split(pemisah) if pemisah else [frasa]
    tak_dikenal = [b for b in bagian if b not in kata]
    bit = entropi(len(bagian), len(kata))
    label, saran = nilai_kekuatan(bit)
    return {
        "jumlah_kata": len(bagian),
        "entropi_bit": bit,
        "kekuatan": label,
        "saran": saran,
        "kata_tak_dikenal": tak_dikenal,
    }
