+++
title = "Technology Lab"
date = "2026-07-13T00:00:00-09:00"
description = "Experimental components that support instrumentation, numerical oceanography, and image-analysis workflows."
status = "Experimental"
weight = 2
+++

# Enabling technology under active development

The Technology Lab collects focused components that support larger Icy Seas systems. These projects are not presented as production products, but they show the technical range behind our consulting and product work.

## SeaState

**SeaState** is a modern C++20 seawater thermodynamics library with stable C and Fortran interfaces. It currently implements a focused native equation-of-state subset based on the TEOS-10/GSW 75-term specific-volume polynomial.

Current status: experimental. It is not a replacement for the complete GSW toolbox, and several state conversions remain approximations or scaffolding.

## serialx

**serialx** is an early R toolkit for communicating with laboratory instruments, sensors, microcontrollers, and embedded devices. A Rust backend provides cross-platform serial-port operations, while R supplies line parsing, logging, SCPI helpers, network connections, diagnostics, and hardware-free mocks.

Current status: early internal release. It is used to explore dependable, testable instrument integrations for field and laboratory systems.

## oracle-builder

**oracle-builder** connects reviewed imagery with lightweight, file-based machine-learning experiments. It supports mask editing, SQLite training datasets, classification and segmentation runs, evaluation, and integration with Pelagia data. It is a private internal tool available through imaging and machine-learning engagements rather than as a standalone product.

## Interested in a component?

These projects may become broader releases as their validation and interfaces mature. [Contact us](/contact/) if one aligns with an instrumentation or scientific-computing need.
