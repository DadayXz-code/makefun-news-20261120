# The World Today — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/DadayXz-code/makefun-news-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/DadayXz-code/makefun-news-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page newspaper front page summing up the world's news of Friday
20 November 2026: 21 stories across 6 regions, drawn as original
illustrations (no photographs, no copied artwork).

## What the program does

`main.ts` (Node 22, standard library only) copies the front page image
shipped beside it (`entry.png`, 1024×1024, 159–163 KB) to
`/output/entry.png`. No network, no clock, no randomness: two runs write
byte-identical output.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## How the image was made

`generate.py` (Python 3 + Pillow, build-time only) draws the whole page:
masthead, ticker strip, lead story, two secondary stories, three story
cards, and a "Day in Brief" column. Every picture is drawn with code —
flat vector-style scenes (a Dnipro bridge under attack, a cyclone spiral,
a radar screen, a falling market chart, the UK and EU flags, a climate
summit globe). Story facts were checked against same-day reporting.

## Stories on the page (21)

- **Lead — Ukraine:** Russia hits three Kyiv bridges in a huge overnight
  barrage (400+ drones, 110+ missiles, 27 ballistic; at least eight killed).
- **Poland:** Russian missiles land in Poland; NATO calls it a grave violation.
- **India:** Cyclone Akvan makes landfall; 300,000 moved to safety.
- **Markets:** AI sell-off deepens — Nasdaq falls for a seventh day.
- **Britain/Europe:** UK and EU close reset deal on food, carbon and youth.
- **Climate:** COP31 draft drops fossil fuels as talks run late.
- **In brief (15):** US Senate 51–48 Iran war-powers vote; Kerch Bridge hit
  a third time; Trump–Xi–Putin meet in Shenzhen; Zelensky's reply; EU's
  "fossil summit" warning; Miliband and Burnham on the EU deal; European
  Commission cyberattack; Europe ready for Ukraine peace talks;
  cost-of-living protests; Lviv station struck; Odisha after Akvan; Polish
  defences scrambled; COP31 fossil-fuel wording; Wall Street's worst week
  since April 2025.

## Entry

Built for make.fun's "Sum up 20 November's world news in one image"
bounty ($250). Payout wallet (see `.makefun/owner.json`):
`GMzu3QobBGo4sYP24deDowGocc47kQeU46eKv619eTcz`.

## License

MIT — see `LICENSE`.
