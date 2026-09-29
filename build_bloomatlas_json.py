"""
Builds bloomatlas.json for the BloomAtlas web app from the merged
Power BI export.

SOURCE: bloom_merged.parquet - one row per species, already cleaned
and modelled in Power BI, exported via DAX Studio.

Source columns (bloom_merged.parquet), and how each maps to the
web app's expected field:

    parquet column              -> JSON field           notes
    ---------------------------------------------------------------
    latin_name                  -> latin_name            passthrough
    genus                       -> genus                 passthrough
    family                      -> family                passthrough
    establishment                -> establishment        passthrough
    taxon_distribution           -> taxon_distribution     passthrough
    flowering_time (12-char y/n) -> flowering_months       reshaped to array
    flower_colours (space-sep)   -> flower_colours         reshaped to array


OUTPUT (bloomatlas.json):
    {
      "species": [
        {
          "latin_name": "...", "genus": "...", "family": "...",
          "establishment": "...",
          "taxon_distribution": "...",
          "flowering_months": ["Jan", "Feb", ...],
          "flower_colours": ["white_cream", ...]
        },
        ...
      ]
    }
"""

import json

import pandas as pd

SOURCE_PARQUET = "bloom_merged.parquet"
OUTPUT_JSON = "bloomatlas.json"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# parquet column -> output JSON field, for the columns that pass through unchanged
PASSTHROUGH_COLUMNS = {
    "latin_name": "latin_name",
    "genus": "genus",
    "family": "family",
    "establishment": "establishment",
    "taxon_distribution": "taxon_distribution",
}

REQUIRED_COLUMNS = list(PASSTHROUGH_COLUMNS) + ["flowering_time", "flower_colours"]


def json_safe(value):
    """Turn pandas/NumPy NA and scalars into JSON-serializable Python values."""
    if value is None or pd.isna(value):
        return None
    if hasattr(value, "item") and not isinstance(value, (str, bytes, list, dict)):
        try:
            return json_safe(value.item())
        except (ValueError, AttributeError):
            pass
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return value
    return str(value)


def flowering_time_to_months(code):
    """'yynnnnnnnnnn' (one y/n per month, Jan through Dec) -> ['Jan','Feb']."""
    code = json_safe(code)
    if not isinstance(code, str) or len(code) != 12:
        return []
    return [month for month, flag in zip(MONTHS, code) if flag.lower() == "y"]


def flower_colour_to_list(value):
    """'white_cream yellow_orange' -> ['white_cream', 'yellow_orange']."""
    value = json_safe(value)
    if not isinstance(value, str) or not value.strip():
        return []
    seen = []
    for token in value.split():
        if token not in seen:
            seen.append(token)
    return seen


def main():
    df = pd.read_parquet(SOURCE_PARQUET)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit(
            f"{SOURCE_PARQUET} is missing expected column(s): {missing}. "
            f"Columns present: {list(df.columns)}"
        )

    rows_in = len(df)

    duplicate_names = df["latin_name"].duplicated().sum()
    if duplicate_names:
        print(f"Warning: {duplicate_names} duplicate latin_name row(s) found - keeping the first of each.")
        df = df.drop_duplicates(subset=["latin_name"], keep="first")

    species_records = []
    empty_months = 0
    for row in df.itertuples(index=False):
        record = {
            json_field: json_safe(getattr(row, parquet_col))
            for parquet_col, json_field in PASSTHROUGH_COLUMNS.items()
        }
        record["flowering_months"] = flowering_time_to_months(row.flowering_time)
        record["flower_colours"] = flower_colour_to_list(row.flower_colours)
        if not record["flowering_months"]:
            empty_months += 1
        species_records.append(record)

    species_records.sort(key=lambda r: (r["latin_name"] or ""))

    output = {"species": species_records}

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, separators=(",", ":"), default=str)

    print(f"Rows read from {SOURCE_PARQUET}: {rows_in:,}")
    print(f"Species written: {len(species_records):,}")
    if empty_months:
        print(f"Note: {empty_months} species have no flowering months marked (all-n flowering_time).")
    print(f"Wrote {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
