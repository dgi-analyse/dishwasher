# Dishwasher

Clean, standardize and validate tabular data.

Dishwasher er en Python-pakke for innlesing, inspeksjon, profilering og standardisering av tabulære datasett. Pakken er bygget på Polars og har spesielt fokus på praktisk datakvalitetsarbeid og norske datasett.

## Funksjonalitet

### Innlesing av filer

Støttede formater:

- CSV
- TSV
- Excel (`.xlsx`, `.xls`)
- Parquet
- JSON
- NDJSON / JSONL

```python
from dishwasher.io import read_table

df = read_table("data.xlsx")
```

### Inspeksjon

Vis grunnleggende informasjon om et datasett.

```python
from dishwasher.inspect import inspect_file

result = inspect_file("data.xlsx")
```

CLI:

```bash
dishwasher inspect data.xlsx
```

### Profilering

Profiler kolonner med:

- datatype
- antall manglende verdier
- antall unike verdier

```python
from dishwasher.profile import profile_file

profile = profile_file("data.xlsx")
```

CLI:

```bash
dishwasher profile data.xlsx
```

### Standardisering

Standardisering av kolonnenavn og verdier.

Eksempler:

```text
Fødselsdato      -> foedselsdato
Kjønn            -> kjoenn
År               -> aar
Org.nr           -> org_nr
```

Funksjonalitet:

- snake_case-kolonnenavn
- håndtering av norske tegn
- trimming av whitespace
- tomme strenger til null
- valgfrie typemoduser

```python
from dishwasher.standardize import standardize_table

df = standardize_table(df)
```

### Fødselsnummer

Verktøy for norske identifikatorer:

- fødselsnummer
- D-nummer
- H-nummer

Eksempler:

```python
from dishwasher.fnr import normalize_fnr
from dishwasher.fnr import validate_fnr
from dishwasher.fnr import inspect_fnr
```

Funksjonalitet:

- normalisering av Excel-skadde fødselsnummer
- kontrollsiffer-validering
- identifisering av FNR/DNR/H-nummer
- uttrekk av fødselsdato
- århundretolkning basert på individnummer
- søk etter sannsynlige fødselsnummerkolonner

## Utvikling

Kjør tester:

```bash
uv run pytest
```

Kjør linting:

```bash
uv run ruff check .
```

Formatter kode:

```bash
uv run ruff format .
```

## Status

Implementert:

- Innlesing
- Inspeksjon
- Profilering
- Standardisering
- Fødselsnummerverktøy

Planlagt:

- Datohåndtering
- Skjemavalidering
- Datakvalitetsrapporter
- Organisasjonsnummer
- Kommunenummer
- Postnummer
