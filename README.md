# FrasaAman

Generator passphrase diceware Bahasa Indonesia — kata sandi kuat yang mudah diingat.

## Kenapa frasa, bukan kata sandi acak?

Kata sandi seperti `Tr0ub4dor&3` susah diingat dan susah diketik, tapi tidak
sekuat kelihatannya. Frasa dari beberapa kata umum yang acak — misalnya
`kopi-gunung-bulan-harimau` — jauh lebih mudah diingat, tapi jauh lebih
sulit ditebak komputer: setiap kata memberi 9 bit entropi, jadi frasa
5 kata ≈ 45 bit dan 6 kata ≈ 54 bit.

Daftar kata FrasaAman berisi **512 kata umum Bahasa Indonesia** yang
dikurasi (satu kata per baris di `frasaaman/kata.txt`). Belum ada daftar
kata diceware Bahasa Indonesia yang baku — daftar ini langkah awalnya.

## Cara pakai

```bash
python3 -m frasaaman buat                  # frasa 5 kata
python3 -m frasaaman buat --kata 6         # frasa 6 kata
python3 -m frasaaman buat --pemisah " "    # pisah dengan spasi
python3 -m frasaaman nilai kopi-gunung-bulan-harimau
python3 -m frasaaman --version
```

## Perintah

| Perintah | Kegunaan |
| --- | --- |
| `buat [--kata N] [--pemisah X]` | Buat frasa baru (bawaan: 5 kata, pemisah `-`) |
| `nilai FRASA [--pemisah X]` | Nilai kekuatan sebuah frasa (entropi + saran) |
| `--version` | Tampilkan versi |

## Rencana

- [x] Day-1: daftar kata 512 kata + generator frasa + CLI `buat`/`nilai`
- [ ] Day-2: opsi angka & huruf besar, mode kata sandi sekali pakai, unit test

## Menjalankan test

```bash
python3 -m unittest discover -s tests
```

## Lisensi

MIT — lihat `LICENSE`.
