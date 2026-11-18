# Talenta Sample Dataset: Calculated Public-Transport Delays at 10 Stops – v1.0

> **Release status: DRAFT – not yet approved for publication.**
> Every item marked `[[TO CLARIFY: …]]` must be decided by the consortium before release. Remove this banner when releasing.

## What this dataset is

This is a sample of the prepared delay dataset from the mFUND project **Talenta** (FKZ 01F2235A–C, 01.01.2023–31.10.2025). It shows the result of the project's GTFS data pipeline:

1. Static and real-time GTFS data were merged.
2. A **delay** column was calculated.
3. Features were encoded for machine-learning–based delay prediction and explainable-AI (SHAP/LIME) analyses.

The dataset was used as an example in the project. It is not a complete record of the source feeds.

**Nature of the data:** derived from real public timetable and real-time data. It is not synthetic. Each row holds the calculated delay of one observed vehicle arrival, together with encoded schedule features. The data contain no personal data.

## File

| File | Rows | Columns | Format |
|---|---|---|---|
| `talenta-gtfs-delay-sample-v1.0.csv` | 1,363 + header | 20 | CSV, comma-separated, UTF-8, CRLF line endings, header row |

The file is identical to the project file `Final_10stops.csv` (SHA-256 in `SHA256SUMS.txt`). A machine-readable column description (W3C CSV on the Web) is in `talenta-gtfs-delay-sample-v1.0.csv-metadata.json`.

## Columns

| Column | Type | Meaning |
|---|---|---|
| `Origin` | text | Name of the stop the vehicle came from (previous stop) |
| `Destination` | text | Name of the stop the vehicle arrived at (GTFS `stop_name`, renamed) |
| `stop_sequence` | integer | GTFS `stop_sequence` of the arrival stop within the trip |
| `route_id` | integer | GTFS `route_id` as used in the source feed (feed-internal ID, not stable across feed versions) |
| `0-3` … `21-24` (8 columns) | 0/1 | One-hot encoded three-hour time slot of the scheduled time, in hours of the day (the final report describes the delay target as arrival-based) |
| `monday` … `sunday` (7 columns) | 0/1 | One-hot encoded day of the week of the trip |
| `delay` | number | Calculated delay: actual arrival time minus scheduled arrival time. Unit: minutes (inferred from the value distribution – integers 0–228, median 1; the unit is not recorded in the pipeline documentation) |

## Coverage

- **Spatial coverage:** 10 origin stops and 11 origin–destination pairs on 18 routes. The stops are in Heidelberg and Mannheim (for example *Heidelberg, Hauptbahnhof*, *Mannheim, Rathaus/REM*). The remaining stop names (for example *Mineralbäder*, *Stöckach*, *Karl-Olga-Krankenhaus*), based on the stop names, appear to be in Stuttgart. The route types (tram, light rail, bus) are not included in the file.
- **Temporal coverage:** collected before 6 May 2024 (date of the data file); the exact collection period is not documented. The file contains no dates. Trips fall on Tuesday to Saturday, between 09:00 and 24:00.

## Provenance and preparation

**Sources** (final report, Teil II, section on data sources and GTFS data collection):

- static and real-time GTFS data from **GTFS für Deutschland** (https://gtfs.de)
- the **Deutsche Bahn** developer portal (https://developer-docs.deutschebahn.com)

The project documentation does not record which of the two sources supplied the data for each of these stops.

**Preparation steps** (as described in the final report):

1. Static GTFS data (planned stops, routes, times) were retrieved.
2. A daily Python script downloaded the real-time data and stored it as JSON; a second script converted it to CSV.
3. The static GTFS files were merged into one table. This table was joined with the real-time data on `trip_id`, `stop_id` and `stop_sequence`.
4. The `delay` column was calculated as actual minus scheduled arrival time.
5. The table was reorganized: `Origin` was added, `stop_name` was renamed `Destination`, and time slots and days of the week were one-hot encoded.
6. A sample of 10 stops was selected for demonstration.

**Ontology:** the GTFS terms used to describe this data come from the Talenta Ontology **v2.0** (`https://github.com/dev-vectorsoft/talenta/ontology/2.0`). The conceptual mapping is:

| CSV column | Ontology term |
|---|---|
| `Origin` | `gtfs:originStop` → `gtfs:Stop` (`stop_name`) |
| `Destination` | `gtfs:destinationStop` → `gtfs:Stop` |
| `stop_sequence` | `gtfs:stopSequence` |
| `route_id` | `gtfs:route` → `gtfs:Route` |
| time slots | derived from `gtfs:arrivalTime` (scheduled) |
| weekdays | `gtfs:monday` … `gtfs:sunday` |
| `delay` | no dedicated term in v2.0 (candidate for a future version) |

The CSV is not RDF. The mapping is for orientation only.

## Data quality and limitations

| Finding | Count |
|---|---|
| Rows without a `delay` value (empty cell) | 77 (cause not documented) |
| Rows without any time-slot flag | 6 |
| Rows identical to another row (expected because of the coarse encoding) | 904 |
| `delay` value range | 0–228 minutes |
| `delay` median | 1 |
| Rows with `delay` ≥ 60 (possible outliers or cancellations) | 22 |

- All 7 rows in the 09:00–12:00 slot have a delay of 185 or 200. Eight rows have exactly 200 in total, 6 of them on route 22656. These values are probably artifacts of the real-time feed (for example a midnight rollover or a cancellation). They are kept unchanged in this release so that the file matches the data used in the project; for analyses, consider excluding them (e.g. `delay >= 185`).
- No negative delays are present, so early arrivals were evidently set to 0 or removed during preparation; which of the two is not documented.
- The data were not validated against operator records.
- Delays reflect the real-time feed as received.
- The sample is small and not representative of a network.
- Not suitable for operational decisions.

## Example

`examples/example_usage.py` loads the file and computes the mean delay per origin–destination pair and per time slot, using Python and pandas. The output of the test run is in `examples/example_output.txt`.

## More data

The complete prepared datasets and an API that provides access to them are not published. Both are available on request from: info@vectorsoft.de.

## Version, license and citation

- **Dataset version:** 1.0
- **Release date:** 2026-11-20
- **License:** CC BY 4.0. This depends on the license of the source GTFS / real-time data and must be compatible with it.
- **Source attribution required by the data sources:** [[TO CLARIFY: exact attribution text from gtfs.de / DB]]
- **Data owner (Dateneigner):** Vectorsoft AG
- **Publisher / data provider:** Vectorsoft AG

**Attribution statement:**

> Talenta Sample Dataset v1.0, mFUND project Talenta (FKZ 01F2235A–C), Vectorsoft AG, Constructor University Bremen gGmbH and Concedra GmbH, funded by the German Federal Ministry of Transport (BMV) within the mFUND program. Contains data derived from www.gtfs.de.

Related publications (from the project's final report):

- Vijaya, A., Gudissa, B. L., Angreani, L. S., & Wicaksono, H. (2024). Predictive analysis of public transportation delays using machine learning models on GTFS data. *2024 IEEE International Conference on Industrial Engineering and Engineering Management (IEEM)*, 450–454. https://doi.org/10.1109/IEEM62345.2024.10857111
- Vijaya, A., Bhattarai, S., Angreani, L. S., & Wicaksono, H. (2024). Enhancing transparency in public transportation delay predictions with SHAP and LIME. *2024 IEEE International Conference on Industrial Engineering and Engineering Management (IEEM)*, 1285–1289. https://doi.org/10.1109/IEEM62345.2024.10857000

## Related offering and contact

- **Ontology:** Talenta Ontology v2.0 on Mobilithek: [[TO CLARIFY: URL]]
- **Technical contact:** info@vectorsoft.de
