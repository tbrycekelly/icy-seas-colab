+++
date = "2025-10-10T16:10:22+02:00"
description = "Other Data Science Products"
external_link = ""
#image = ""
project_id = "other"
short_description = ""
title = "Data Science Products"

[[participants]]
    name = "Thomas Bryce Kelly"
    is_member = true
    id = "Thomas Bryce Kelly"

+++

## Simple Mapper
 A Simple mapping library for R. This library is self contained with some optional linkages to other libraries/datasets.

Inspiration for this project originated back in 2017 when we were first exploring options for mapping and visualizing spatial data in the R universe. What we found, and largely still find, was an ecosystem of GIS-centric libraries with far more horse-power than we needed.

Power is great, except when it comes with a learning curve and inflexibility. Finding the then-current libraries were unable to reliably spit out a map of our data points with clear cause-and-effect structures (e.g., do this to add an arrow or do this to add a label), we decided to build our own library suited to the task of making maps simpler.

If you like this, then I'd recommend checking out an accessory package I've written for adding bathymetry (or topography) to maps: [SimpleBathy](https://github.com/tbrycekelly/SimpleBathy). You may also be intersted in color palettes suitable for scientific data presentation: [batlow](https://github.com/tbrycekelly/batlow).

---

## SimpleBathy

An add on package for [SimpleMapper](https://github.com/tbrycekelly/SimpleMapper) to provide bathymetric data and capabilities.

You may also be interested in a color palette package available based on the excellent _batlow_ set of palettes for scientific data presentation: [batlow package](https://github.com/tbrycekelly/batlow).

---

## batlow
This is an easy to use wrapper package for the wonderful, scientifically accurate color palettes curated by Fabio Crameri and others (see references). This package seeks to make these color palettes available to the R community outside of ggplot2 (see the [scico](https://github.com/thomasp85/scico) package for ggplot2 compatible implementation) in a manner consistent with the excellent _pals_ package [link](https://cran.r-project.org/web/packages/pals/index.html).

