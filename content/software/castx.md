+++
title = "castx"
date = "2026-07-13T00:00:00-09:00"
description = "Transparent processing of Sea-Bird SBE 911/911plus CTD data into inspectable SQLite projects and open scientific exports."
status = "Public alpha"
weight = 1
+++

# Reproducible CTD processing without the black box

`castx` converts raw Sea-Bird SBE 911/911plus cruise files into an inspectable project database, derived oceanographic variables, processing reports, and standards-oriented exports.

<div class="portfolio-meta">
<p><strong>Status:</strong> Alpha; representative cruise validation is ongoing</p>
<p><strong>Availability:</strong> Public source under the MIT License</p>
<p><strong>Best for:</strong> Oceanographers who want processing steps, source files, calibration metadata, and validation state preserved together</p>
</div>

## Current capabilities

- Immutable source-file ingest with SHA-256 hashes
- XMLCON metadata and calibration extraction
- Common SBE-style HEX scan decoding
- Temperature, conductivity, pressure, salinity, density, and TEOS-10 derived variables
- Transparent processing recipes and recorded QC flags
- Pressure-binned profiles
- CSV, Parquet, and NetCDF export
- Reference CNV comparison reports
- Markdown processing reports
- Command-line and guided interactive workflows

## Honest validation

`castx` records processing and comparison results with explicit validation states. The current release targets SBE 911/911plus casts; final bottle-sample calibrations, real-time acquisition, a graphical interface, and broad Sea-Bird instrument support remain outside the MVP.

We welcome research groups with representative cruise data who want to compare results against trusted processing references.

<div class="button-row">
<a class="btn btn-primary" href="https://github.com/Icy-Seas-Co-Laboratory/castx">View source and documentation</a>
<a class="btn btn-default" href="/contact/">Discuss validation or integration</a>
</div>
