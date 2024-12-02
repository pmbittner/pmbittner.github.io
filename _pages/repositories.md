---
layout: page
permalink: /repositories/
title: Repositories
description:
nav: true
nav_order: 4
---

Here, I showcase some of my notable Github repositories.

{% if site.data.repositories.github_repos %}

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.liquid repository=repo %}
  {% endfor %}
</div>

{% endif %}

---

## Some Stats for Fun

{% if site.data.repositories.github_users %}

The following overview is missing the stars of the projects I moved to the [Github organization of our research project VariantSync](https://github.com/VariantSync/):
<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for user in site.data.repositories.github_users %}
    {% include repository/repo_user.liquid username=user %}
  {% endfor %}
</div>
{% if site.repo_trophies.enabled %}
  {% for user in site.data.repositories.github_users %}
  <div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo_trophies.liquid username=user %}
  </div>
   {% endfor %}
{% endif %}

{% endif %}
