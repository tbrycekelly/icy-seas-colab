+++
title = "FixPoint"
date = "2026-07-13T00:00:00-09:00"
description = "Offline-first event, position, and operational logging for oceanographic cruises and field programs."
status = "Field-test MVP"
weight = 2
+++

# Preserve what happened, when, and where

FixPoint is an offline-capable scientific event logging system for oceanographic operations. It gives watch standers, technicians, and science teams one structured record of deployments, recoveries, positions, notes, corrections, and instrument context.

<div class="portfolio-meta">
<p><strong>Status:</strong> Field-test MVP under active development</p>
<p><strong>Availability:</strong> Pilot deployments and collaborative evaluation</p>
<p><strong>Best for:</strong> Research cruises and remote field programs that need dependable local operation and a coherent post-mission record</p>
</div>

## Built around operational sequences

Cruise events are more than isolated timestamps. A CTD cast, net tow, or instrument deployment follows a sequence of valid actions. FixPoint models those sequences explicitly so the interface can show operators what may happen next while the backend preserves the rules.

- Backend-enforced state-machine transitions
- Append-only event actions with UUIDv7 identifiers
- UTC timestamps and canonical latitude/longitude fields
- Corrections that preserve the original record
- Sequence notes and configurable action types
- Configurable CTD, net-tow, and instrument workflows

## Position and instrument context

FixPoint can attach operator-provided coordinates or the nearest recent position observation to actions that require a location. The MVP includes NMEA 0183 RMC and GGA parsing, diagnostic packet ingestion, and UDP listener support, with initial TCP and serial workflows.

The shipboard dashboard shows recent activity, system state, and available position context. Its default map uses bundled Natural Earth data so core operations do not require an internet connection.

## Exports and operational resilience

- CSV event-action exports
- JSONL timeline exports
- GeoJSON spatial exports
- Local SQLite operation with WAL mode
- SQLite database and raw-packet backup workflows
- Plain latitude/longitude fallback if the map cannot initialize

## Example workflow

Before a cruise, a team defines its instruments and valid sequences in readable TOML configuration. During operations, the watch creates a CTD sequence and records deploy, bottom, and recover actions. FixPoint attaches UTC time and position, retains later corrections without overwriting the original actions, and produces timeline and spatial exports for post-cruise reconciliation.

## Current boundaries

FixPoint is ready for controlled field testing, not unattended production deployment. Full authentication, durable listener supervision across restarts, high-rate packet queueing, detailed offline basemaps, Postgres backups, and complete browser end-to-end testing remain planned work. Every deployment should include a hardware, GPS/clock, backup, and operator smoke test.

## Plan a pilot

We are seeking research teams willing to test FixPoint against real operational sequences and provide structured feedback before broader release.

<div class="button-row">
<a class="btn btn-primary" href="/contact/">Discuss a FixPoint pilot</a>
<a class="btn btn-default" href="https://github.com/Icy-Seas-Co-Laboratory/FixPoint">View public source</a>
</div>
