"""Test daftar kata FrasaAman (frasaaman/kata.py)."""

import unittest

from frasaaman.kata import jumlah_kata, muat_kata


class TestKata(unittest.TestCase):
    def test_jumlah_512(self):
        self.assertEqual(len(muat_kata()), 512)

    def test_semua_unik(self):
        kata = muat_kata()
        self.assertEqual(len(set(kata)), len(kata))

    def test_semua_huruf_kecil(self):
        for kata in muat_kata():
            self.assertEqual(kata, kata.lower(), kata)

    def test_semua_alfabetik(self):
        for kata in muat_kata():
            self.assertTrue(kata.isalpha(), kata)

    def test_panjang_kata_minimal_dua(self):
        for kata in muat_kata():
            self.assertGreaterEqual(len(kata), 2, kata)

    def test_muat_kata_cache(self):
        # Pemanggilan kedua mengembalikan objek yang sama (di-cache).
        self.assertIs(muat_kata(), muat_kata())

    def test_jumlah_kata(self):
        self.assertEqual(jumlah_kata(), 512)


if __name__ == "__main__":
    unittest.main()
