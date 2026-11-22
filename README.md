# The World Today — Sunday, 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/vahad98/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/vahad98/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-page evening newspaper (1024×1024) summing up the world's news of
Sunday 22 November 2026 in a single image. Entry for the make.fun
competition [news-image-20261122](https://make.fun/competitions/news-image-20261122).

## Stories on the page

- **The Gulf (hero):** Iran hits US bases in Bahrain — Tehran claims
  missiles and drones struck two Patriot radars; Bahrain says an
  industrial site burned, with no casualties.
- **Markets:** S&P 500 −3.7% as the AI sell-off spreads.
- **Climate:** COP31 in overtime — Antalya talks pass a second day past
  deadline, deadlocked over fossil fuels.
- **Mexico:** Cartel boss seized — Mexico captures FBI most-wanted
  "El Chapo Isidro" in Sinaloa; 11 killed in the raid.
- **Summit:** Three leaders, one table — Trump, Xi and Putin meet in
  Shenzhen and agree to talk on nuclear risks.
- **Also today:** EU–Indonesia trade deal (730 million people);
  Russia hits Zelensky's hometown, Ukraine hits a Russian ship;
  magnitude 6.9 quake in Peru's Andes; GTA VI sets a $3.79bn
  first-day sales record; factory fire in Indonesia kills 3, 36 missing;
  boat carrying mourners capsizes in Nigeria, 24 dead.

## How to build

```sh
python3 compose.py        # renders entry.png (1024x1024, <= 1 MiB)
```

`compose.py` reads the four photo panels in `assets/` (generated for this
entry, no text in them) and draws every word on the page with Pillow
(Noto Serif / Noto Sans). It is deterministic: running it twice produces
byte-identical output.

## How to run the entry

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/
```

## Verification

```sh
python3 compose.py
python3 -c "from PIL import Image; im = Image.open('entry.png'); print(im.size, im.format)"
ls -l entry.png                          # must be <= 1048576 bytes
python3 compose.py && sha256sum entry.png
python3 compose.py && sha256sum entry.png   # hashes must match
MAKEFUN_OUTPUT_DIR=/tmp/out1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/out2 python3 main.py
cmp /tmp/out1/entry.png /tmp/out2/entry.png  # copies must be identical
```

## License

MIT — see [LICENSE](LICENSE). The four photo panels in `assets/` were
generated for this entry and are released under the same license.
