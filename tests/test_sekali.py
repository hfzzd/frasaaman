"""Test kata sandi sekali pakai (frasaaman/sekali.py).

Memakai rng palsu yang deterministik supaya isi kata sandi bisa
diprediksi persis tanpa bergantung pada angka acak.
"""

import math
import unittest

from frasaaman.sekali import (
    KARAKTER,
    PANJANG_MAKS,
    PANJANG_MIN,
    buat_sandi_sekali_pakai,
    entropi_sandi,
)


class RngPalsu:
    """RNG deterministik: choice mengembalikan karakter berurutan."""

    def __init__(self, karakter="Ab1!"):
        self._karakter = karakter
        self._indeks = 0

    def choice(self, _seq):
        huruf = self._karakter[self._indeks % len(self._karakter)]
        self._indeks += 1
        return huruf


class TestBuatSandiSekaliPakai(unittest.TestCase):
    def test_panjang_bawaan_16(self):
        sandi = buat_sandi_sekali_pakai(rng=RngPalsu())
        self.assertEqual(sandi, "Ab1!Ab1!Ab1!Ab1!")
        self.assertEqual(len(sandi), 16)

    def test_panjang_min_8(self):
        sandi = buat_sandi_sekali_pakai(panjang=8, rng=RngPalsu())
        self.assertEqual(sandi, "Ab1!Ab1!")
        self.assertEqual(len(sandi), 8)

    def test_panjang_maks_64(self):
        sandi = buat_sandi_sekali_pakai(panjang=64, rng=RngPalsu())
        self.assertEqual(len(sandi), 64)
        self.assertEqual(sandi, "Ab1!" * 16)

    def test_hanya_karakter_yang_diizinkan(self):
        sandi = buat_sandi_sekali_pakai(panjang=32, rng=RngPalsu("aZ09#"))
        self.assertEqual(len(sandi), 32)
        self.assertTrue(all(h in KARAKTER for h in sandi), sandi)

    def test_acak_bawaan_panjang_dan_karakter_benar(self):
        sandi = buat_sandi_sekali_pakai(panjang=16)
        self.assertEqual(len(sandi), 16)
        self.assertTrue(all(h in KARAKTER for h in sandi), sandi)

    def test_tolak_di_luar_rentang(self):
        for buruk in (PANJANG_MIN - 1, PANJANG_MAKS + 1, 0, -5, 100):
            with self.subTest(buruk=buruk), self.assertRaises(ValueError):
                buat_sandi_sekali_pakai(panjang=buruk, rng=RngPalsu())

    def test_tolak_bukan_int(self):
        for buruk in ("16", 16.0, True, None):
            with self.subTest(buruk=buruk), self.assertRaises(ValueError):
                buat_sandi_sekali_pakai(panjang=buruk, rng=RngPalsu())


class TestEntropiSandi(unittest.TestCase):
    def test_enam_belas_karakter_sekitar_105_bit(self):
        # 16 karakter x log2(94) = 104,87 bit -> ~105 bit.
        self.assertAlmostEqual(entropi_sandi(16), 105, delta=0.5)
        self.assertAlmostEqual(entropi_sandi(16), 16 * math.log2(len(KARAKTER)))

    def test_delapan_karakter_sekitar_52_bit(self):
        self.assertAlmostEqual(entropi_sandi(8), 8 * math.log2(len(KARAKTER)))

    def test_dua_puluh_empat_karakter_sekitar_157_bit(self):
        self.assertAlmostEqual(entropi_sandi(24), 24 * math.log2(len(KARAKTER)))
        self.assertAlmostEqual(entropi_sandi(24), 157, delta=0.5)

    def test_entropi_naik_sebanding_panjang(self):
        self.assertAlmostEqual(entropi_sandi(32), 2 * entropi_sandi(16))


if __name__ == "__main__":
    unittest.main()
