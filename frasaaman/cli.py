"""CLI FrasaAman: `buat` frasa baru dan `nilai` frasa yang sudah ada."""

import argparse
import sys

from . import __version__
from .frasa import buat_frasa, entropi, nilai_frasa, nilai_kekuatan, rincian_entropi
from .kata import (ekspor_kata, jumlah_kata, jumlah_semua_kata,
                   muat_kata_pengguna, tambah_kata)
from .sekali import PANJANG_MAKS, PANJANG_MIN, buat_sandi_sekali_pakai, entropi_sandi


def _parser():
    parser = argparse.ArgumentParser(
        prog="frasaaman",
        description="Generator passphrase diceware Bahasa Indonesia.",
    )
    parser.add_argument("--version", action="version",
                        version="%(prog)s " + __version__)
    sub = parser.add_subparsers(dest="perintah")

    buat = sub.add_parser("buat", help="buat frasa baru")
    buat.add_argument("--kata", type=int, default=5,
                      help="jumlah kata dalam frasa (bawaan: 5)")
    buat.add_argument("--pemisah", default="-",
                      help="pemisah antar kata (bawaan: -)")
    buat.add_argument("--angka", action="store_true",
                      help="tambahkan satu digit acak (0-9) di akhir frasa (+~3,3 bit)")
    buat.add_argument("--kapital", action="store_true",
                      help="kapitalkan huruf pertama satu kata acak (+~2,3 bit)")
    buat.add_argument("--jumlah", type=int, default=1,
                      help="jumlah frasa yang dibuat sekaligus (1-20, bawaan: 1)")

    nilai = sub.add_parser("nilai", help="nilai kekuatan sebuah frasa")
    nilai.add_argument("frasa", help="frasa yang dinilai, mis. kopi-gunung-bulan")
    nilai.add_argument("--pemisah", default="-",
                       help="pemisah antar kata (bawaan: -)")

    tambah = sub.add_parser("tambah-kata",
                            help="tambah kata kamu sendiri ke daftar kata")
    tambah.add_argument("kata", nargs="+",
                        help="satu kata atau lebih (huruf kecil a-z, minimal 3 huruf)")

    sekali = sub.add_parser("sekali-pakai",
                            help="buat kata sandi sekali pakai (tidak disimpan)")
    sekali.add_argument("--panjang", type=int, default=16,
                        help=f"panjang kata sandi ({PANJANG_MIN}-{PANJANG_MAKS}, bawaan: 16)")

    ekspor = sub.add_parser("ekspor-kata",
                            help="ekspor daftar kata ke berkas (satu kata per baris)")
    ekspor.add_argument("berkas", nargs="?", default="kata-frasaaman.txt",
                        help="berkas tujuan (bawaan: kata-frasaaman.txt)")
    return parser


def main(argv=None):
    args = _parser().parse_args(argv)
    if args.perintah == "buat":
        if not 1 <= args.jumlah <= 20:
            print("Maaf: --jumlah harus antara 1 dan 20.", file=sys.stderr)
            return 1
        try:
            frasa_list = [
                buat_frasa(jumlah=args.kata, pemisah=args.pemisah,
                           angka=args.angka, kapital=args.kapital)
                for _ in range(args.jumlah)
            ]
        except ValueError as err:
            print(f"Maaf: {err}.", file=sys.stderr)
            return 1
        bit = entropi(args.kata, jumlah_semua_kata(),
                      angka=args.angka, kapital=args.kapital)
        label, saran = nilai_kekuatan(bit)
        rincian = rincian_entropi(args.kata, jumlah_semua_kata(),
                                  angka=args.angka, kapital=args.kapital)
        for i, frasa in enumerate(frasa_list):
            if i:
                print()
            print(frasa)
            print(f"Entropi: {bit:.0f} bit ({rincian}) — {label}")
        print(f"Saran: {saran}.")
        return 0
    if args.perintah == "nilai":
        try:
            hasil = nilai_frasa(args.frasa, pemisah=args.pemisah)
        except ValueError as err:
            print(f"Maaf: {err}.", file=sys.stderr)
            return 1
        print(f"Frasa: {args.frasa}")
        print(f"Kata: {hasil['jumlah_kata']} — entropi {hasil['entropi_bit']:.0f} bit "
              f"— {hasil['kekuatan']}")
        if hasil["kata_tak_dikenal"]:
            tak_dikenal = ", ".join(hasil["kata_tak_dikenal"])
            print(f"Catatan: kata ini tidak ada di daftar FrasaAman: {tak_dikenal}.")
        print(f"Saran: {hasil['saran']}.")
        return 0
    if args.perintah == "tambah-kata":
        ditambahkan, ditolak = tambah_kata(*args.kata)
        if ditambahkan:
            gabung = ", ".join(ditambahkan)
            print(f"Kata ditambahkan ({len(ditambahkan)}): {gabung}.")
            print(f"Daftar kata sekarang: {jumlah_semua_kata()} kata "
                  f"({jumlah_kata()} bawaan + "
                  f"{len(muat_kata_pengguna())} kata kamu).")
        for kata, alasan in ditolak:
            print(f"Dilewati: {kata} — {alasan}.", file=sys.stderr)
        if not ditambahkan:
            print("Maaf: tidak ada kata baru yang ditambahkan.", file=sys.stderr)
            return 1
        return 0
    if args.perintah == "sekali-pakai":
        try:
            sandi = buat_sandi_sekali_pakai(panjang=args.panjang)
        except ValueError as err:
            print(f"Maaf: {err}.", file=sys.stderr)
            return 1
        bit = entropi_sandi(args.panjang)
        label, _ = nilai_kekuatan(bit)
        print(sandi)
        print(f"Entropi: {bit:.0f} bit — {label}")
        print("Hanya tampil sekali — catat atau salin sekarang.")
        print("FrasaAman tidak menyimpan kata sandi ini di mana pun.")
        return 0
    if args.perintah == "ekspor-kata":
        try:
            jumlah = ekspor_kata(args.berkas)
        except OSError as err:
            print(f"Maaf: tidak bisa menulis {args.berkas} ({err}).",
                  file=sys.stderr)
            return 1
        kata_kamu = len(muat_kata_pengguna())
        print(f"{jumlah} kata diekspor ke {args.berkas} "
              f"({jumlah_kata()} bawaan + {kata_kamu} kata kamu).")
        return 0
    print("FrasaAman — generator passphrase diceware Bahasa Indonesia.")
    kata_kamu = len(muat_kata_pengguna())
    if kata_kamu:
        print(f"Daftar kata: {jumlah_kata()} kata umum + {kata_kamu} kata kamu.")
    else:
        print(f"Daftar kata: {jumlah_kata()} kata umum.")
    print("Perintah: `buat` untuk frasa baru, `nilai FRASA` untuk menilai frasa,")
    print("`tambah-kata KATA` untuk menambah kata kamu sendiri,")
    print("`sekali-pakai` untuk kata sandi sekali pakai,")
    print("`ekspor-kata [BERKAS]` untuk mengekspor daftar kata.")
    print("Lihat `frasaaman --help` untuk semua pilihan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
