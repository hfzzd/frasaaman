"""Test CLI end-to-end via subprocess (python3 -m frasaaman ...).

Semua subprocess memakai env FRASAAMAN_KATA_PENGGUNA yang menunjuk
berkas /tmp (bukan berkas kata pengguna asli di mesin), supaya jumlah
kata dan entropi yang dikunci test Day-1 (512 kata) tidak berubah.
Test yang menulis kata pengguna memakai berkas /tmp-nya sendiri.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_BERKAS_KATA_KOSONG = None


def setUpModule():
    global _BERKAS_KATA_KOSONG
    fd, jalur = tempfile.mkstemp(prefix="frasaaman-test-", suffix=".txt")
    os.close(fd)
    _BERKAS_KATA_KOSONG = jalur


def tearDownModule():
    if _BERKAS_KATA_KOSONG:
        try:
            os.unlink(_BERKAS_KATA_KOSONG)
        except FileNotFoundError:
            pass


def jalankan(*args, berkas_kata=None):
    """Jalankan CLI; `berkas_kata` menunjuk berkas kata pengguna (/tmp).

    Tanpa `berkas_kata`, dipakai berkas /tmp kosong supaya test tidak
    membaca berkas kata pengguna asli di mesin.
    """
    env = dict(os.environ)
    env["FRASAAMAN_KATA_PENGGUNA"] = str(berkas_kata or _BERKAS_KATA_KOSONG)
    return subprocess.run(
        [sys.executable, "-m", "frasaaman", *args],
        cwd=ROOT, capture_output=True, text=True, timeout=30, env=env,
    )


class _BerkasKataPengguna:
    """Mixin: tiap test punya berkas kata pengguna sendiri di /tmp."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.berkas_kata = Path(self._tmp.name) / "kata-pengguna.txt"

    def tearDown(self):
        self._tmp.cleanup()


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
        self.assertIn("0.2.0", hasil.stdout)

    def test_tanpa_perintah(self):
        hasil = jalankan()
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertIn("512 kata", hasil.stdout)

    def test_tanpa_perintah_tampilkan_kata_kamu(self):
        with tempfile.TemporaryDirectory() as tmp:
            berkas = Path(tmp) / "kata-pengguna.txt"
            jalankan("tambah-kata", "markisa", "kelengkeng",
                     berkas_kata=berkas)
            hasil = jalankan(berkas_kata=berkas)
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertIn("512 kata umum + 2 kata kamu", hasil.stdout)


class TestCliTambahKata(_BerkasKataPengguna, unittest.TestCase):
    def test_tambah_kata_berhasil(self):
        hasil = jalankan("tambah-kata", "markisa", "kelengkeng",
                         berkas_kata=self.berkas_kata)
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertIn("Kata ditambahkan (2): markisa, kelengkeng.",
                      hasil.stdout)
        self.assertIn("514 kata", hasil.stdout)
        self.assertEqual(
            self.berkas_kata.read_text(encoding="utf-8"),
            "markisa\nkelengkeng\n")
        # kata pengguna langsung dikenali perintah nilai
        hasil = jalankan("nilai", "markisa-kelengkeng-kopi",
                         berkas_kata=self.berkas_kata)
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertIn("Kata: 3", hasil.stdout)
        self.assertIn("27 bit", hasil.stdout)
        self.assertNotIn("tidak ada di daftar", hasil.stdout)

    def test_tambah_kata_duplikat(self):
        jalankan("tambah-kata", "markisa", berkas_kata=self.berkas_kata)
        hasil = jalankan("tambah-kata", "markisa",
                         berkas_kata=self.berkas_kata)
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("Dilewati: markisa", hasil.stderr)
        self.assertIn("Maaf: tidak ada kata baru", hasil.stderr)

    def test_tambah_kata_duplikat_bawaan(self):
        hasil = jalankan("tambah-kata", "kopi",
                         berkas_kata=self.berkas_kata)
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("Dilewati: kopi", hasil.stderr)
        self.assertIn("daftar bawaan", hasil.stderr)

    def test_tambah_kata_terlalu_pendek(self):
        hasil = jalankan("tambah-kata", "ab",
                         berkas_kata=self.berkas_kata)
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("Dilewati: ab", hasil.stderr)
        self.assertIn("pendek", hasil.stderr)

    def test_tambah_kata_dengan_angka(self):
        hasil = jalankan("tambah-kata", "kopi2",
                         berkas_kata=self.berkas_kata)
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("Dilewati: kopi2", hasil.stderr)
        self.assertIn("huruf kecil", hasil.stderr)


class TestCliSekaliPakai(unittest.TestCase):
    def test_sekali_pakai_panjang_bawaan(self):
        hasil = jalankan("sekali-pakai")
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        baris = hasil.stdout.splitlines()
        self.assertEqual(len(baris[0]), 16)
        self.assertIn("Entropi: 105 bit", hasil.stdout)
        self.assertIn("Sangat kuat", hasil.stdout)
        self.assertIn("tidak menyimpan", hasil.stdout)

    def test_sekali_pakai_panjang_24(self):
        hasil = jalankan("sekali-pakai", "--panjang", "24")
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertEqual(len(hasil.stdout.splitlines()[0]), 24)
        self.assertIn("Entropi: 157 bit", hasil.stdout)

    def test_sekali_pakai_panjang_4_ditolak(self):
        hasil = jalankan("sekali-pakai", "--panjang", "4")
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("Maaf", hasil.stderr)


class TestCliEksporKata(_BerkasKataPengguna, unittest.TestCase):
    def test_ekspor_kata_tanpa_kata_pengguna(self):
        tujuan = Path(self._tmp.name) / "ekspor.txt"
        hasil = jalankan("ekspor-kata", str(tujuan),
                         berkas_kata=self.berkas_kata)
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertIn("512 kata diekspor", hasil.stdout)
        baris = tujuan.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(baris), 512)

    def test_ekspor_kata_isi_dan_jumlah_dengan_kata_pengguna(self):
        jalankan("tambah-kata", "markisa", "kelengkeng",
                 berkas_kata=self.berkas_kata)
        tujuan = Path(self._tmp.name) / "ekspor.txt"
        hasil = jalankan("ekspor-kata", str(tujuan),
                         berkas_kata=self.berkas_kata)
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertIn("514 kata diekspor", hasil.stdout)
        self.assertIn("512 bawaan + 2 kata kamu", hasil.stdout)
        baris = tujuan.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(baris), 514)
        self.assertEqual(baris[-2:], ["markisa", "kelengkeng"])


if __name__ == "__main__":
    unittest.main()
