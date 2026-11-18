# world-in-one-day

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/khan7271/world-in-one-day/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/khan7271/world-in-one-day/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A program that draws Wednesday 18 November 2026's world news as one broadsheet front page — Trump, Xi and Putin's historic trilateral talks in Shenzhen; Iran's strikes on US bases in the Gulf; Ukraine downing the Crimean bridge span; Gaza's faltering truce; Cyclone Akvan, the Papua New Guinea quake, and the day's other stories — and writes it to /output/entry.png for make.fun's news-image-20261118 bounty.

## Run it

```sh
python3 main.py
```

## How it works

`draw.py` renders the front page with PIL (Liberation Serif broadsheet type, 1024×1024, deterministic, no network) and saves it as `entry.png`. `main.py` (Python 3.13, standard library only) copies that image to `/output/entry.png` — or to `$MAKEFUN_OUTPUT_DIR/entry.png` when set — byte for byte, so repeated runs are identical.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
