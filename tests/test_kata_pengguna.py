"""Test kata pengguna, daftar gabungan, dan ekspor kata (frasaaman/kata.py).

Setiap test memakai berkas kata pengguna sendiri di /tmp lewat env
FRASAAMAN_KATA_PENGGUNA, supaya berkas kata pengguna asli di mesin
tidak mengubah hasil test.
"""

import os
import tempfile
import unittest
from pathlib import Path

from frasaaman.kata import (
    ekspor_kata,
    jumlah_kata,
    jumlah_semua_kata,
    muat_kata,
    muat_kata_pengguna,
    muat_semua_kata,
    tambah_kata,
)


class TestKataPengguna(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.berkas_kata = Path(self._tmp.name) / "kata-pengguna.txt"
        self._env_lama = os.environ.get("FRASAAMAN_KATA_PENGGUNA")
        os.environ["FRASAAMAN_KATA_PENGGUNA"] = str(self.berkas_kata)

    def tearDown(self):
        if self._env_lama is None:
            os.environ.pop("FRASAAMAN_KATA_PENGGUNA", None)
        else:
            os.environ["FRASAAMAN_KATA_PENGGUNA"] = self._env_lama
        self._tmp.cleanup()

    def test_tambah_kata_valid(self):
        ditambahkan, ditolak = tambah_kata("markisa")
        self.assertEqual(ditambahkan, ["markisa"])
        self.assertEqual(ditolak, [])
        self.assertEqual(self.berkas_kata.read_text(encoding="utf-8"),
                         "markisa\n")

    def test_tambah_beberapa_kata_sekaligus(self):
        ditambahkan, ditolak = tambah_kata("markisa", "kelengkeng")
        self.assertEqual(ditambahkan, ["markisa", "kelengkeng"])
        self.assertEqual(ditolak, [])
        self.assertEqual(muat_kata_pengguna(), ["markisa", "kelengkeng"])

    def test_tambah_kata_dinormalisasi_huruf_kecil(self):
        ditambahkan, _ = tambah_kata("Markisa")
        self.assertEqual(ditambahkan, ["markisa"])

    def test_tolak_duplikat_kata_pengguna(self):
        tambah_kata("markisa")
        ditambahkan, ditolak = tambah_kata("markisa")
        self.assertEqual(ditambahkan, [])
        self.assertEqual(len(ditolak), 1)
        self.assertEqual(ditolak[0][0], "markisa")
        self.assertIn("kata kamu", ditolak[0][1])

    def test_tolak_duplikat_daftar_bawaan(self):
        ditambahkan, ditolak = tambah_kata("kopi")
        self.assertEqual(ditambahkan, [])
        self.assertEqual(len(ditolak), 1)
        self.assertIn("daftar bawaan", ditolak[0][1])

    def test_tolak_kata_terlalu_pendek(self):
        for pendek in ("ab", "a", ""):
            with self.subTest(pendek=pendek):
                ditambahkan, ditolak = tambah_kata(pendek)
                self.assertEqual(ditambahkan, [])
                self.assertIn("pendek", ditolak[0][1])

    def test_tolak_kata_dengan_angka_atau_huruf_besar(self):
        # "Kopi" dilowercase dulu jadi "kopi" -> duplikat bawaan;
        # "kopi2" mengandung angka -> ditolak karena bukan huruf saja.
        _, ditolak_angka = tambah_kata("kopi2")
        self.assertIn("huruf kecil", ditolak_angka[0][1])
        _, ditolak_besar = tambah_kata("Kopi")
        self.assertIn("daftar bawaan", ditolak_besar[0][1])

    def test_tambah_campuran_valid_dan_ditolak(self):
        ditambahkan, ditolak = tambah_kata("markisa", "ab", "kopi")
        self.assertEqual(ditambahkan, ["markisa"])
        self.assertEqual([k for k, _ in ditolak], ["ab", "kopi"])

    def test_muat_kata_pengguna_kosong_bila_berkas_belum_ada(self):
        self.assertEqual(muat_kata_pengguna(), [])

    def test_muat_semua_kata_gabungan_tanpa_duplikat(self):
        tambah_kata("markisa", "kelengkeng")
        gabungan = muat_semua_kata()
        self.assertEqual(len(gabungan), 514)
        self.assertEqual(len(set(gabungan)), 514)
        self.assertEqual(gabungan[:512], muat_kata())
        self.assertEqual(gabungan[512:], ["markisa", "kelengkeng"])

    def test_jumlah_semua_kata(self):
        self.assertEqual(jumlah_semua_kata(), 512)
        tambah_kata("markisa")
        self.assertEqual(jumlah_semua_kata(), 513)
        self.assertEqual(jumlah_kata(), 512)


class TestEksporKata(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.berkas_kata = Path(self._tmp.name) / "kata-pengguna.txt"
        self._env_lama = os.environ.get("FRASAAMAN_KATA_PENGGUNA")
        os.environ["FRASAAMAN_KATA_PENGGUNA"] = str(self.berkas_kata)

    def tearDown(self):
        if self._env_lama is None:
            os.environ.pop("FRASAAMAN_KATA_PENGGUNA", None)
        else:
            os.environ["FRASAAMAN_KATA_PENGGUNA"] = self._env_lama
        self._tmp.cleanup()

    def test_ekspor_tanpa_kata_pengguna(self):
        tujuan = Path(self._tmp.name) / "ekspor.txt"
        jumlah = ekspor_kata(str(tujuan))
        self.assertEqual(jumlah, 512)
        baris = tujuan.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(baris), 512)
        self.assertEqual(baris, muat_kata())

    def test_ekspor_isi_dan_jumlah_dengan_kata_pengguna(self):
        tambah_kata("markisa", "kelengkeng")
        tujuan = Path(self._tmp.name) / "ekspor.txt"
        jumlah = ekspor_kata(str(tujuan))
        self.assertEqual(jumlah, 514)
        baris = tujuan.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(baris), 514)
        self.assertEqual(baris, muat_semua_kata())
        self.assertEqual(baris[-2:], ["markisa", "kelengkeng"])


if __name__ == "__main__":
    unittest.main()
