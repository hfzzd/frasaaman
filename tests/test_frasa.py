"""Test generator dan penilai frasa (frasaaman/frasa.py).

Memakai rng palsu yang deterministik supaya hasil frasa bisa
diprediksi persis tanpa bergantung pada angka acak.
"""

import math
import unittest

from frasaaman.frasa import (
    buat_frasa,
    entropi,
    nilai_frasa,
    nilai_kekuatan,
    rincian_entropi,
)


class RngPalsu:
    """RNG deterministik: choice mengembalikan kata berurutan,
    randrange mengembalikan digit/posisi yang tetap."""

    def __init__(self, kata=("kopi", "gunung", "bulan", "harimau", "bintang"),
                 digit=7, posisi_kapital=1):
        self._kata = kata
        self._indeks = 0
        self.digit = digit
        self.posisi_kapital = posisi_kapital

    def choice(self, _seq):
        kata = self._kata[self._indeks % len(self._kata)]
        self._indeks += 1
        return kata

    def randrange(self, n):
        if n == 10:
            return self.digit
        return self.posisi_kapital


class TestBuatFrasa(unittest.TestCase):
    def test_lima_kata_bawaan(self):
        frasa = buat_frasa(rng=RngPalsu())
        self.assertEqual(frasa, "kopi-gunung-bulan-harimau-bintang")

    def test_jumlah_enam_kata(self):
        frasa = buat_frasa(jumlah=6, rng=RngPalsu())
        self.assertEqual(frasa, "kopi-gunung-bulan-harimau-bintang-kopi")

    def test_satu_kata(self):
        self.assertEqual(buat_frasa(jumlah=1, rng=RngPalsu()), "kopi")

    def test_pemisah_spasi(self):
        frasa = buat_frasa(pemisah=" ", rng=RngPalsu())
        self.assertEqual(frasa, "kopi gunung bulan harimau bintang")

    def test_tolak_jumlah_nol(self):
        with self.assertRaises(ValueError):
            buat_frasa(jumlah=0, rng=RngPalsu())

    def test_tolak_jumlah_negatif(self):
        with self.assertRaises(ValueError):
            buat_frasa(jumlah=-3, rng=RngPalsu())

    def test_tolak_jumlah_bukan_int(self):
        for buruk in ("5", 2.5, True, None):
            with self.subTest(buruk=buruk), self.assertRaises(ValueError):
                buat_frasa(jumlah=buruk, rng=RngPalsu())

    def test_angka_tambah_digit_di_akhir(self):
        frasa = buat_frasa(angka=True, rng=RngPalsu())
        self.assertEqual(frasa, "kopi-gunung-bulan-harimau-bintang7")

    def test_kapital_kapitalkan_satu_kata(self):
        frasa = buat_frasa(kapital=True, rng=RngPalsu())
        self.assertEqual(frasa, "kopi-Gunung-bulan-harimau-bintang")

    def test_angka_dan_kapital(self):
        frasa = buat_frasa(angka=True, kapital=True, rng=RngPalsu())
        self.assertEqual(frasa, "kopi-Gunung-bulan-harimau-bintang7")


class TestEntropi(unittest.TestCase):
    def test_lima_kata_45_bit(self):
        self.assertEqual(entropi(5), 45.0)

    def test_enam_kata_54_bit(self):
        self.assertEqual(entropi(6), 54.0)

    def test_angka_tambah_log2_10(self):
        self.assertAlmostEqual(entropi(5, angka=True), 45 + math.log2(10))

    def test_kapital_tambah_log2_jumlah(self):
        self.assertAlmostEqual(entropi(5, kapital=True), 45 + math.log2(5))

    def test_angka_kapital_enam_kata(self):
        self.assertAlmostEqual(
            entropi(6, angka=True, kapital=True),
            54 + math.log2(10) + math.log2(6))

    def test_rincian_entropi(self):
        self.assertEqual(rincian_entropi(5), "5 kata x 9 bit")
        rincian = rincian_entropi(5, angka=True, kapital=True)
        self.assertIn("digit 3,3 bit", rincian)
        self.assertIn("kapital 2,3 bit", rincian)


class TestNilaiKekuatan(unittest.TestCase):
    def test_batas_label(self):
        kasus = [
            (0, "Lemah"), (27.9, "Lemah"),
            (28, "Cukup"), (44.9, "Cukup"),
            (45, "Kuat"), (59.9, "Kuat"),
            (60, "Sangat kuat"), (100, "Sangat kuat"),
        ]
        for bit, label in kasus:
            with self.subTest(bit=bit):
                self.assertEqual(nilai_kekuatan(bit)[0], label)


class TestNilaiFrasa(unittest.TestCase):
    def test_frasa_dikenal(self):
        hasil = nilai_frasa("kopi-gunung-bulan-harimau")
        self.assertEqual(hasil["jumlah_kata"], 4)
        self.assertEqual(hasil["entropi_bit"], 36.0)
        self.assertEqual(hasil["kekuatan"], "Cukup")
        self.assertEqual(hasil["kata_tak_dikenal"], [])

    def test_kata_tak_dikenal_dilaporkan(self):
        hasil = nilai_frasa("kopi-xyz-bulan")
        self.assertEqual(hasil["jumlah_kata"], 3)
        self.assertEqual(hasil["kata_tak_dikenal"], ["xyz"])

    def test_frasa_kosong_ditolak(self):
        with self.assertRaises(ValueError):
            nilai_frasa("")
        with self.assertRaises(ValueError):
            nilai_frasa("   ")


if __name__ == "__main__":
    unittest.main()
