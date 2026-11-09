# Event weather context

## Selected scope

Enrich an individual report with a bounded weather snapshot for its location and
observation time. This is event context, not connected report/case history. Weather
is optional enrichment: unavailable data remains unknown and does not prevent intake
or an assessment without weather. It does not establish eligibility for routine advice.

The image classifier receives the photo only. A proposed second model interprets its
unaltered candidate scores, the farmer note and this snapshot. Model selection and
integration remain open. Farm/nearby reports, prior assessments, treatments and cases
stay outside both models; code/DMN and technicians use that connected history.
The [routing worksheet](DMN-RULE-WORKSHEET.md#assessment-and-routing-boundary) owns
assessment and routing responsibilities.

## Variables and evidence

| Variable | Selected use | Evidence and limit |
| --- | --- | --- |
| Daily minimum/maximum air temperature | Core context for cold and heat exposure; include relevant frost warnings when available. | [Coffee frost experiment](https://www.scielo.br/j/babt/a/XyT63Q5Vs8CgVcLW3GGw4Km/?lang=en) found differences in frost response among accessions. Grid air temperature is not leaf temperature or proof of frost injury; no universal injury threshold is adopted. |
| Daily rainfall total | Core context; retain individual days rather than only a window total. | [Cenicafé waterlogging experiment](https://www.mdpi.com/2073-4395/12/6/1270) measured adverse effects under imposed waterlogging in seedlings. Rainfall alone cannot establish saturated soil, poor drainage or the cause of symptoms. |
| Relative humidity summary | Core moisture context; propose daily mean/max of hourly values. | [Brazilian rust study](https://link.springer.com/article/10.1007/s00704-026-06384-8) reports associations with humidity and leaf wetness under differing yield conditions. Ambient humidity is not measured leaf-wetness duration or a diagnostic threshold. |
| Maximum wind gust and its time | Core context for possible acute exposure; confirm provider availability. | [Coffee wind experiment](https://apct.sede.embrapa.br/pab/en/article/view/15050) found growth effects and mechanical damage in young plants under sustained wind. Gusts are an engineering choice for investigating sudden damage, not a validated predictor from that experiment. Its nursery wind speeds are not adopted as field thresholds. |
| Frost, hail and storm alerts/events | Optional, source permitting; retain type, affected area, valid time and warning/observation distinction. | [Cenicafé hail observations](https://publicaciones.cenicafe.org/index.php/avances_tecnicos/issue/view/1674) document physical damage. [CPTEC warning criteria](https://s0.cptec.inpe.br/webcptec/sites/tempo/assets/pdf/criterios_avisos_meteorologicos.pdf) describe probabilistic regional warnings. Area/time overlap indicates possible exposure, not confirmed farm damage. |

Defer sunshine hours and average wind speed from the first snapshot. They are not
irrelevant, but interpreting them adds exposure assumptions. [Coffee irradiance
experiments](https://ps.ueb.cas.cz/artkey/phs-199713-0012_photoinhibition-and-recovery-of-photosynthesis-in-coffea-arabica-and-c-canephora.php)
show photoinhibition responses; sunshine duration does not measure irradiance at an
individual shaded leaf. Average wind can obscure a short gust. Radiation, canopy
shade and sustained wind can be evaluated later if the demonstration needs them.

These sources justify relevance and limitations, not a diagnosis rule or treatment.
Reported experimental conditions are not prototype severity cutoffs.

## Acquisition and reproducibility

Candidate numeric source: [Open-Meteo historical weather documentation](https://open-meteo.com/en/docs/historical-weather-api).
It documents temperature, precipitation, humidity and wind variables using gridded
weather/reanalysis. The source is a candidate, not an integrated or tested dependency.
Check model coverage, recent-data delay, missing variables, licence/attribution and
usage limits before selecting an endpoint. Do not infer historical warnings or observed
hail from a general weather code; a suitable alert/archive source remains unselected.

- Fetch server-side using the report's location and observation time. Retain requested
  location, returned grid location/elevation/resolution where supplied, provider/model,
  units, timestamps/timezone, retrieval time and missing values. Raw coordinates need
  not be sent onward to an assessment model.
- Save an immutable snapshot and reference its version from the assessment. Derive
  summaries in code; keep the underlying intervals and aggregation method traceable.
  Re-fetching creates a new snapshot rather than silently changing earlier evidence.
- Use only weather intervals ending at or before observation time. A completed daily
  total for the observation date can include later weather; use elapsed hourly data or
  previous complete days instead. Forecasts must be identified separately from estimates
  of past conditions; reconstructed data retrieved later is not a real-time record.
- Proposed demonstration window: the preceding seven days, with recent daily values
  retained. This is an engineering starting point, not a validated disease window.
  Window selection remains open before implementation. [Brazilian rust literature](https://www.mdpi.com/2073-4395/12/2/496)
  describes latency measured in weeks, so a short window cannot explain every visible
  infection. Do not attribute symptoms to yesterday's rain by default.

## Assumptions and uncertainty

- Weather represents estimated conditions near the farm, not an on-farm sensor.
  Terrain, shelter and canopy can make plant exposure differ from the grid estimate.
- Intake currently uses simulated observation time at photo selection. Attaching
  real weather to an uploaded dataset photo therefore supplies scenario context,
  not verified conditions when that photo was taken. Label that combination synthetic;
  do not claim it validates weather-aware diagnosis.
- Preserve separate indicators for image limitations, missing farmer information,
  weather age/resolution/coverage and assessment contradictions. No combined numerical
  certainty factor or calibrated disease probability is established.
- Weather may support an alternative explanation; it must not turn a classifier's
  limited label set into proof of frost, hail or other unsupported injury. Candidate
  scores remain visible; unavailable model coverage remains explicit.

## Planned verification and current evidence

Check location/time alignment, units, missing/stale data, aggregation boundaries,
immutable snapshot linkage and history exclusion from model requests. Compare the
same reports with and without weather; report actual outcomes and contradictory
examples. Synthetic context demonstrates workflow only unless independently suitable
reference truth supports assessment scoring.

Sources were consulted for planning on 9 November 2026. No weather data has been
fetched, no alert archive selected, no environmental thresholds validated and no
weather-aware model experiments run. This document changes no BPMN or application code.
