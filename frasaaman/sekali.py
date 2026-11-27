"""Kata sandi sekali pakai: dibuat, ditampilkan sekali, tidak disimpan.

Berbeda dengan frasa diceware yang dirancang untuk diingat, kata sandi
sekali pakai dirancang untuk disalin sekali lalu dibuang — mis. kata
sandi sementara untuk akun yang dibagikan sebentar, atau kode darurat.
FrasaAman TIDAK menyimpan kata sandi ini di mana pun; setelah layar
tertutup, satu-satunya salinan ada di tangan pengguna.
"""

import math
import secrets
import string

KARAKTER = string.ascii_letters + string.digits + string.punctuation
PANJANG_MIN = 8
PANJANG_MAKS = 64


def buat_sandi_sekali_pakai(panjang=16, rng=None):
    """Buat kata sandi acak sepanjang `panjang` karakter.

    Memakai `secrets` (CSPRNG) secara bawaan; `rng` hanya untuk test
    (objek dengan metode `choice`). Panjang 8-64 karakter.
    """
    if (not isinstance(panjang, int) or isinstance(panjang, bool)
            or not PANJANG_MIN <= panjang <= PANJANG_MAKS):
        raise ValueError(
            f"panjang kata sandi harus bilangan bulat {PANJANG_MIN}-{PANJANG_MAKS}")
    acak = rng if rng is not None else secrets.SystemRandom()
    return "".join(acak.choice(KARAKTER) for _ in range(panjang))


def entropi_sandi(panjang):
    """Perkiraan entropi (bit) kata sandi sepanjang `panjang` karakter."""
    return panjang * math.log2(len(KARAKTER))
