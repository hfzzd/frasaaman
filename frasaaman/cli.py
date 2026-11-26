"""CLI FrasaAman: `buat` frasa baru dan `nilai` frasa yang sudah ada."""

import argparse
import sys

from . import __version__
from .frasa import buat_frasa, entropi, nilai_frasa, nilai_kekuatan, rincian_entropi
from .kata import jumlah_kata


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

    nilai = sub.add_parser("nilai", help="nilai kekuatan sebuah frasa")
    nilai.add_argument("frasa", help="frasa yang dinilai, mis. kopi-gunung-bulan")
    nilai.add_argument("--pemisah", default="-",
                       help="pemisah antar kata (bawaan: -)")
    return parser


def main(argv=None):
    args = _parser().parse_args(argv)
    if args.perintah == "buat":
        try:
            frasa = buat_frasa(jumlah=args.kata, pemisah=args.pemisah,
                               angka=args.angka, kapital=args.kapital)
        except ValueError as err:
            print(f"Maaf: {err}.", file=sys.stderr)
            return 1
        bit = entropi(args.kata, jumlah_kata(),
                      angka=args.angka, kapital=args.kapital)
        label, saran = nilai_kekuatan(bit)
        rincian = rincian_entropi(args.kata, jumlah_kata(),
                                  angka=args.angka, kapital=args.kapital)
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
    print("FrasaAman — generator passphrase diceware Bahasa Indonesia.")
    print(f"Daftar kata: {jumlah_kata()} kata umum.")
    print("Perintah: `buat` untuk frasa baru, `nilai FRASA` untuk menilai frasa.")
    print("Lihat `frasaaman --help` untuk semua pilihan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
