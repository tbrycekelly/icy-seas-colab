+++
title = "Open Scientific Software"
description = "Transparent tools and enabling technology for ocean data, pelagic imaging, instrumentation, and reproducible research."
+++

# Open scientific software

We build software whose assumptions, transformations, and limitations can be inspected. Some systems are fully open source, some have public development repositories while licensing matures, and some remain private components used within Icy Seas engagements. We state that distinction explicitly so visitors know what they can evaluate, reuse, or access through collaboration.

<div class="portfolio-meta">
<p><strong>Open source:</strong> Source and a reuse license are publicly available.</p>
<p><strong>Public source:</strong> Development is visible, but broader reuse terms or production readiness may still be evolving.</p>
<p><strong>Private development:</strong> Available through pilots, consulting, or a connected commercial interface.</p>
</div>

## Ocean data & operations

Tools for preserving operational context and making oceanographic processing transparent.

<div class="portfolio-grid portfolio-grid-3">
<article class="portfolio-card product-card">
<span class="status-badge status-alpha">Open source · alpha</span>
<h3>castx</h3>
<p>Processes raw Sea-Bird SBE 911/911plus CTD data into inspectable SQLite projects, recorded recipes, comparison reports, and CSV, Parquet, or NetCDF exports.</p>
<a href="/software/castx/">Explore castx &rarr;</a>
</article>
<article class="portfolio-card product-card">
<span class="status-badge status-pilot">Public source · field-test MVP</span>
<h3>FixPoint</h3>
<p>Offline-first event, position, and sequence logging for oceanographic cruises, including append-only actions, corrections, exports, and local backups.</p>
<a href="/product/fixpoint/">Explore FixPoint &rarr;</a>
</article>
<article class="portfolio-card">
<h3>Applied ocean operations</h3>
<p>These tools can be configured together with instrument integration, cruise workflow design, operator training, and post-mission data handoff.</p>
<a href="/solutions/ocean-operations/">View the Ocean Operations solution &rarr;</a>
</article>
</div>

## Pelagic imaging & machine learning

Connected software for moving from large image collections to reviewable observations and reproducible data products.

<div class="portfolio-grid portfolio-grid-3">
<article class="portfolio-card product-card">
<span class="status-badge status-active">Open-source backend</span>
<h3>Pelagia</h3>
<p>An analysis server for image and video ingestion, preprocessing, segmentation, ROI refinement, workers, metadata, and durable scientific artifacts.</p>
<a href="https://github.com/Icy-Seas-Co-Laboratory/Pelagia">View backend source &rarr;</a>
</article>
<article class="portfolio-card product-card">
<span class="status-badge status-preview">Closed-source frontend</span>
<h3>PelagiaView</h3>
<p>The connected commercial web GUI for frame inspection, ROI review, queue management, quality control, and export.</p>
<a href="https://pelagia.studio/">Visit pelagia.studio &rarr;</a>
</article>
<article class="portfolio-card">
<span class="status-badge status-preview">Private development</span>
<h3>oracle-builder</h3>
<p>Mask editing, SQLite training datasets, model experiments, evaluation, and integration with reviewed Pelagia imagery.</p>
<a href="/software/technology-lab/#oracle-builder">Read about oracle-builder &rarr;</a>
</article>
</div>

## Instrumentation & technical computing

Focused components that support larger field, laboratory, and analysis systems.

<div class="portfolio-grid portfolio-grid-3">
<article class="portfolio-card">
<span class="status-badge status-preview">Experimental</span>
<h3>SeaState</h3>
<p>A modern C++20 seawater thermodynamics library with C and Fortran interfaces and a focused TEOS-10/GSW equation-of-state subset.</p>
<a href="/software/technology-lab/#seastate">Read about SeaState &rarr;</a>
</article>
<article class="portfolio-card">
<span class="status-badge status-preview">Early release</span>
<h3>serialx</h3>
<p>An R toolkit with a Rust backend for serial, TCP, and UDP communication with instruments, sensors, microcontrollers, and embedded devices.</p>
<a href="/software/technology-lab/#serialx">Read about serialx &rarr;</a>
</article>
<article class="portfolio-card">
<h3>Technology Lab</h3>
<p>Earlier components remain in the lab while their validation, interfaces, documentation, and release model mature.</p>
<a href="/software/technology-lab/">Explore the Technology Lab &rarr;</a>
</article>
</div>

## Research data infrastructure

Datum is a private-preview research data workspace rather than an open-source release. It appears here because it demonstrates the same inspectable approach to metadata, file revisions, dataset versions, audit history, and reproducible export packages.

<div class="button-row"><a class="btn btn-default" href="/product/datum/">Learn about Datum</a><a class="btn btn-primary" href="/solutions/research-data-systems/">Explore Research Data Systems</a></div>

## Collaborate or contribute

Public repositories welcome appropriate issues, validation results, and technical discussion. For pilots, integrations, private components, or applied deployment support, [contact Icy Seas](/contact/).
