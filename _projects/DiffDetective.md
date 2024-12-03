---
layout: page
title: DiffDetective
description: variability-aware source code differencing and large scale empirical evaluations on git repositories
img: assets/img/DiffDetective.png
img-background: "white"
importance: 2
category: Software Variability and Configuration
related_publications: true
language: Java
publications:
  - key: BSM+:FSE24Companion
  - key: BSG+:SPLC23
  - key: GBST:VaMoS24
  - key: BTS+:ESECFSE22
---

<div class="row justify-content-sm-center">
    <div class="col-sm-2 mt-3 mt-md-0">
    </div>
    <div class="col-sm-8 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/DiffDetective.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-2 mt-3 mt-md-0">
    </div>
</div>

DiffDetective is our Java library for variability-aware source code differencing:
It helps in understanding how a change (e.g., a commit) to a code base with static variability, such as C preprocessor annotations, has changed.
Therefore, the library parses a generic diff - such as the text-based diff in the image above - into a variability-aware data-structure, where changes to variability annotations are distinguished from changes to source code.
To get an overview of variability-aware differencing and what our library has to offer, please check out our demonstrations paper {% cite BSM+:FSE24Companion %} as well as our Github repository:

<div class="row justify-content-sm-center">
{% include repository/repo.liquid repository="VariantSync/DiffDetective" %}
</div>

We used DiffDetective as a framework for empirical evaluations in multiple studies {% cite BSG+:SPLC23 %}, {% cite GBST:VaMoS24 %}, {% cite BTS+:ESECFSE22 %}.
