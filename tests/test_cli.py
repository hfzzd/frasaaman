"""Test CLI end-to-end via subprocess (python3 -m frasaaman ...)."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def jalankan(*args):
    return subprocess.run(
        [sys.executable, "-m", "frasaaman", *args],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
    )


class TestCliBuat(unittest.TestCase):
    def test_buat_lima_kata(self):
        hasil = jalankan("buat")
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        baris = hasil.stdout.splitlines()
        self.assertEqual(len(baris[0].split("-")), 5)
        self.assertIn("Entropi: 45 bit", hasil.stdout)
        self.assertIn("Kuat", hasil.stdout)

    def test_buat_enam_kata(self):
        hasil = jalankan("buat", "--kata", "6")
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertEqual(len(hasil.stdout.splitlines()[0].split("-")), 6)
        self.assertIn("Entropi: 54 bit", hasil.stdout)

    def test_buat_jumlah_tiga(self):
        hasil = jalankan("buat", "--jumlah", "3")
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertEqual(hasil.stdout.count("Entropi:"), 3)

    def test_buat_angka_kapital(self):
        hasil = jalankan("buat", "--angka", "--kapital")
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        frasa = hasil.stdout.splitlines()[0]
        self.assertTrue(frasa[-1].isdigit(), frasa)
        self.assertTrue(any(h.isupper() for h in frasa), frasa)
        self.assertIn("Entropi:", hasil.stdout)

    def test_buat_kata_nol_error_ramah(self):
        hasil = jalankan("buat", "--kata", "0")
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("Maaf", hasil.stderr)

    def test_buat_jumlah_nol_error_ramah(self):
        hasil = jalankan("buat", "--jumlah", "0")
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("Maaf", hasil.stderr)


class TestCliNilai(unittest.TestCase):
    def test_nilai_frasa_dikenal(self):
        hasil = jalankan("nilai", "kopi-gunung-bulan-harimau")
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertIn("Kata: 4", hasil.stdout)
        self.assertIn("36 bit", hasil.stdout)
        self.assertIn("Cukup", hasil.stdout)
        self.assertNotIn("tidak ada di daftar", hasil.stdout)

    def test_nilai_frasa_tak_dikenal(self):
        hasil = jalankan("nilai", "abc-def")
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertIn("18 bit", hasil.stdout)
        self.assertIn("Lemah", hasil.stdout)
        self.assertIn("tidak ada di daftar", hasil.stdout)


class TestCliUmum(unittest.TestCase):
    def test_version(self):
        hasil = jalankan("--version")
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertIn("0.1.0", hasil.stdout)

    def test_tanpa_perintah(self):
        hasil = jalankan()
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertIn("512 kata", hasil.stdout)


if __name__ == "__main__":
    unittest.main()
