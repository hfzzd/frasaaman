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

Buat frasa baru (5 kata, 45 bit):

```bash
$ python3 -m frasaaman buat
besi-berani-gizi-ladang-laptop
Entropi: 45 bit (5 kata x 9 bit) — Kuat
Saran: sudah kuat untuk sebagian besar keperluan.
```

Frasa 6 kata (54 bit):

```bash
$ python3 -m frasaaman buat --kata 6
gigih-mengajar-asteroid-gunung-gratis-pelukis
Entropi: 54 bit (6 kata x 9 bit) — Kuat
Saran: sudah kuat untuk sebagian besar keperluan.
```

Tambah digit dan huruf kapital (51 bit):

```bash
$ python3 -m frasaaman buat --angka --kapital
agar-sedih-Pelukis-serabi-menjaga4
Entropi: 51 bit (5 kata x 9 bit + digit 3,3 bit + kapital 2,3 bit) — Kuat
Saran: sudah kuat untuk sebagian besar keperluan.
```

Buat tiga frasa sekaligus:

```bash
$ python3 -m frasaaman buat --jumlah 3
belajar-mahal-masuk-jujur-mobil
Entropi: 45 bit (5 kata x 9 bit) — Kuat

bank-olahraga-kamis-jupiter-jalan
Entropi: 45 bit (5 kata x 9 bit) — Kuat

bahasa-sabtu-hemat-komik-kertas
Entropi: 45 bit (5 kata x 9 bit) — Kuat
Saran: sudah kuat untuk sebagian besar keperluan.
```

Nilai frasa yang sudah ada:

```bash
$ python3 -m frasaaman nilai kopi-gunung-bulan-harimau
Frasa: kopi-gunung-bulan-harimau
Kata: 4 — entropi 36 bit — Cukup
Saran: cukup untuk akun biasa, tambah 1 kata untuk akun penting.

$ python3 -m frasaaman nilai abc-def
Frasa: abc-def
Kata: 2 — entropi 18 bit — Lemah
Catatan: kata ini tidak ada di daftar FrasaAman: abc, def.
Saran: tambah kata — frasa 4 kata atau kurang mudah ditebak.
```

## Perintah

| Perintah | Kegunaan |
| --- | --- |
| `buat [--kata N] [--pemisah X] [--angka] [--kapital] [--jumlah N]` | Buat frasa baru (bawaan: 5 kata, pemisah `-`, 1 frasa) |
| `nilai FRASA [--pemisah X]` | Nilai kekuatan sebuah frasa (entropi + saran) |
| `--version` | Tampilkan versi (0.1.0) |

Opsi `buat`:

| Opsi | Kegunaan |
| --- | --- |
| `--kata N` | Jumlah kata dalam frasa (bawaan: 5) |
| `--pemisah X` | Pemisah antar kata (bawaan: `-`, mis. `" "`) |
| `--angka` | Tambahkan satu digit acak (0-9) di akhir frasa (+~3,3 bit) |
| `--kapital` | Kapitalkan huruf pertama satu kata acak (+~2,3 bit) |
| `--jumlah N` | Jumlah frasa yang dibuat sekaligus (1-20, bawaan: 1) |

## Skala kekuatan

| Entropi | Label | Arti |
| --- | --- | --- |
| < 28 bit | Lemah | Frasa 3 kata atau kurang — mudah ditebak, tambah kata |
| 28–44 bit | Cukup | Cukup untuk akun biasa, tambah 1 kata untuk akun penting |
| 45–59 bit | Kuat | Sudah kuat untuk sebagian besar keperluan |
| ≥ 60 bit | Sangat kuat | Sangat kuat — simpan baik-baik |

Contoh: frasa 5 kata = 45 bit (Kuat), 6 kata = 54 bit (Kuat),
6 kata + angka + kapital ≈ 60 bit (ambang Sangat kuat).

## Menjalankan test

```bash
python3 -m unittest discover -s tests
```

37 test lolos: daftar kata (512 kata, unik, huruf kecil semua, cache),
generator frasa (rng deterministik, tolak jumlah 0/negatif/bukan-int,
entropi, batas label kekuatan, kata tak dikenal), dan CLI end-to-end
(`buat`, `buat --kata 6`, `buat --jumlah 3`, `buat --angka --kapital`,
`nilai` frasa dikenal/tak dikenal, error ramah exit 1, `--version`).

## Rencana

- [x] Day-1: daftar kata 512 kata + generator frasa + CLI `buat`/`nilai`
  + opsi `--angka`/`--kapital` + opsi `--jumlah` + unit test + README
- [ ] Day-2: daftar kata yang bisa ditambah pengguna + mode kata sandi
  sekali pakai + ekspor kata

## Lisensi

MIT — lihat `LICENSE`.
