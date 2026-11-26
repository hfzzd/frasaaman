"""CLI FrasaAman: `buat` frasa baru dan `nilai` frasa yang sudah ada."""

import argparse
import sys

from . import __version__
from .frasa import buat_frasa, nilai_frasa
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

    nilai = sub.add_parser("nilai", help="nilai kekuatan sebuah frasa")
    nilai.add_argument("frasa", help="frasa yang dinilai, mis. kopi-gunung-bulan")
    nilai.add_argument("--pemisah", default="-",
                       help="pemisah antar kata (bawaan: -)")
    return parser


def main(argv=None):
    args = _parser().parse_args(argv)
    if args.perintah == "buat":
        try:
            frasa = buat_frasa(jumlah=args.kata, pemisah=args.pemisah)
        except ValueError as err:
            print(f"Maaf: {err}.", file=sys.stderr)
            return 1
        hasil = nilai_frasa(frasa, pemisah=args.pemisah)
        print(frasa)
        print(f"Entropi: {hasil['entropi_bit']:.0f} bit "
              f"({hasil['jumlah_kata']} kata x 9 bit) — {hasil['kekuatan']}")
        print(f"Saran: {hasil['saran']}.")
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
