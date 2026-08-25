# Iside — proposta logo

Palette scelta da Alessandro: **#FF0065** (255 0 101) dentro le forme,
**#FF0016** (255 0 22) sul bordo. Il bordo non è un contorno decorativo: è la
regola che tiene insieme wordmark e marchio, dove il colore più caldo sta
sempre all'esterno e quello più saturo all'interno.

| File | Cos'è |
| --- | --- |
| `logo-iside-wordmark.svg` | ISIDE, tracciati veri, riempimento core + bordo rim |
| `logo-iside-lockup.svg` | wordmark + SYSTEMS sotto |
| `logo-iside-mark.svg` | quadrato annidato — quello che il sito usa già, ricolorato |
| `logo-iside-mark-alt.svg` | alternativa: la I del wordmark su blocco pieno |
| `proposta-logo.png` | il foglio di presentazione |

Il font è **Archivo Black** (SIL Open Font License), scaricato in `fonts/` e
convertito in tracciati: il logo non dipende da un font installato e non porta
con sé nessuna questione di licenza. Con Arial Black, che era la scelta ovvia
su macOS, non sarebbe stato così.

Rigenerare:

    python3 build_logo.py      # SVG + PNG (serve fonttools, cairosvg)
    python3 sheet.py           # il foglio di presentazione
    python3 explore.py         # le tre direzioni iniziali

Il sito non è stato toccato: qui c'è solo la proposta.
