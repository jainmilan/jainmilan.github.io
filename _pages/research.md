---
# title: "research."
layout: archive
permalink: /research/
classes: wide
---

{% assign default_research_image = "/assets/images/posts/research-abstract-teaser.png" %}

<div class="research-view-tabs" role="tablist" aria-label="Research views">
  <button class="research-view-tab is-active" type="button" id="research-tab-ml-ai" role="tab" aria-selected="true" aria-controls="research-panel-ml-ai" data-research-view-tab="ml-ai">ML/AI Areas</button>
  <button class="research-view-tab" type="button" id="research-tab-applications" role="tab" aria-selected="false" aria-controls="research-panel-applications" data-research-view-tab="applications">Application Areas</button>
  <button class="research-view-tab" type="button" id="research-tab-projects" role="tab" aria-selected="false" aria-controls="research-panel-projects" data-research-view-tab="projects">Projects</button>
</div>

<section class="research-view-panel is-active" id="research-panel-ml-ai" role="tabpanel" aria-labelledby="research-tab-ml-ai" data-research-view-panel="ml-ai">
  <header class="research-section__header">
    <h2>ML/AI Areas</h2>
  </header>

  <div class="research-area-grid">
    {% for area in site.data.research_areas.ml_ai %}
      {% capture area_tag_slugs %}{% for tag in area.tags %}{{ tag | slugify }} {% endfor %}{% endcapture %}
      <article class="research-area-card" tabindex="0" role="button" aria-label="Show {{ area.title | escape }} projects" data-area-filter="{{ area_tag_slugs | strip }}">
        <img src="{{ default_research_image | relative_url }}" alt="">
        <div class="research-area-card__content">
          <h3>{{ area.title }}</h3>
          <ul>
            {% assign has_projects = false %}
            {% assign sorted_projects = site.projects | sort: "title" %}
            {% for project in sorted_projects %}
              {% assign matched_project = false %}
              {% for tag in area.tags %}
                {% if project.tags contains tag %}
                  {% assign matched_project = true %}
                {% endif %}
              {% endfor %}
              {% if matched_project %}
                {% assign has_projects = true %}
                <li><a href="{{ project.url | relative_url }}">{{ project.title }}</a></li>
              {% endif %}
            {% endfor %}
            {% unless has_projects %}
              <li>No projects tagged yet.</li>
            {% endunless %}
          </ul>
        </div>
      </article>
    {% endfor %}
  </div>
</section>

<section class="research-view-panel" id="research-panel-applications" role="tabpanel" aria-labelledby="research-tab-applications" data-research-view-panel="applications" hidden>
  <header class="research-section__header">
    <h2>Application Areas</h2>
  </header>

  <div class="research-area-grid">
    {% for area in site.data.research_areas.applications %}
      {% capture area_tag_slugs %}{% for tag in area.tags %}{{ tag | slugify }} {% endfor %}{% endcapture %}
      <article class="research-area-card" tabindex="0" role="button" aria-label="Show {{ area.title | escape }} projects" data-area-filter="{{ area_tag_slugs | strip }}">
        <img src="{{ default_research_image | relative_url }}" alt="">
        <div class="research-area-card__content">
          <h3>{{ area.title }}</h3>
          <ul>
            {% assign has_projects = false %}
            {% assign sorted_projects = site.projects | sort: "title" %}
            {% for project in sorted_projects %}
              {% assign matched_project = false %}
              {% for tag in area.tags %}
                {% if project.tags contains tag %}
                  {% assign matched_project = true %}
                {% endif %}
              {% endfor %}
              {% if matched_project %}
                {% assign has_projects = true %}
                <li><a href="{{ project.url | relative_url }}">{{ project.title }}</a></li>
              {% endif %}
            {% endfor %}
            {% unless has_projects %}
              <li>No projects tagged yet.</li>
            {% endunless %}
          </ul>
        </div>
      </article>
    {% endfor %}
  </div>
</section>

<section class="research-view-panel" id="research-panel-projects" role="tabpanel" aria-labelledby="research-tab-projects" data-research-view-panel="projects" hidden>
  <header class="research-section__header">
    <h2>Projects</h2>
  </header>

  <div class="project-browser" data-project-browser>
    <div class="project-filter-cloud" aria-label="Filter projects by tag">
      <button class="project-filter-pill is-active project-filter-pill--all" type="button" data-project-filter="all" aria-pressed="true">All projects</button>
      {% assign project_tags = site.projects | map: "tags" | compact | join: "," | split: "," | uniq | sort %}
      {% for tag in project_tags %}
        {% assign clean_tag = tag | strip %}
        {% if clean_tag != "" %}
          {% assign tag_slug = clean_tag | slugify %}
          {% assign tag_count = 0 %}
          {% for project in site.projects %}
            {% if project.tags contains clean_tag %}
              {% assign tag_count = tag_count | plus: 1 %}
            {% endif %}
          {% endfor %}
          {% assign cloud_size = tag_count %}
          {% if cloud_size > 3 %}{% assign cloud_size = 3 %}{% endif %}
          {% assign color_index = forloop.index0 | modulo: 6 | plus: 1 %}
          <button class="project-filter-pill project-filter-pill--{{ cloud_size }} project-filter-pill--color-{{ color_index }}" type="button" data-project-filter="{{ tag_slug }}" aria-pressed="false">{{ clean_tag }}</button>
        {% endif %}
      {% endfor %}
    </div>

    <div class="project-card-grid">
      {% assign sorted_projects = site.projects | sort: "title" %}
      {% for project in sorted_projects %}
        {% capture project_tag_slugs %}{% for tag in project.tags %}{{ tag | slugify }} {% endfor %}{% endcapture %}
        <article class="project-card" data-project-row data-tags="{{ project_tag_slugs | strip }}">
          {% if project.header.teaser %}
            <a class="project-card__image" href="{{ project.url | relative_url }}" aria-label="{{ project.title | markdownify | strip_html | strip_newlines | escape_once }}">
              <img src="{{ project.header.teaser | relative_url }}" alt="">
            </a>
          {% endif %}
          <div class="project-card__body">
            <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
            {% if project.excerpt %}<p>{{ project.excerpt | markdownify | strip_html }}</p>{% endif %}
            {% if project.tags %}
              <div class="project-card__tags" aria-label="Project tags">
                {% for tag in project.tags limit:4 %}
                  <span>{{ tag }}</span>
                {% endfor %}
              </div>
            {% endif %}
          </div>
        </article>
      {% endfor %}
    </div>

    <p class="project-empty" data-project-empty hidden>No projects match this tag.</p>
  </div>
</section>

<script>
  (function () {
    var viewTabs = document.querySelectorAll("[data-research-view-tab]");
    var viewPanels = document.querySelectorAll("[data-research-view-panel]");

    function activateView(view) {
      viewTabs.forEach(function (tab) {
        var isActive = tab.getAttribute("data-research-view-tab") === view;
        tab.classList.toggle("is-active", isActive);
        tab.setAttribute("aria-selected", isActive ? "true" : "false");
      });

      viewPanels.forEach(function (panel) {
        var isActive = panel.getAttribute("data-research-view-panel") === view;
        panel.classList.toggle("is-active", isActive);
        panel.hidden = !isActive;
      });
    }

    viewTabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        activateView(tab.getAttribute("data-research-view-tab"));
      });
    });

    var projectBrowser = document.querySelector("[data-project-browser]");

    if (!projectBrowser) {
      return;
    }

    var filters = projectBrowser.querySelectorAll("[data-project-filter]");
    var rows = projectBrowser.querySelectorAll("[data-project-row]");
    var empty = projectBrowser.querySelector("[data-project-empty]");
    var areaCards = document.querySelectorAll("[data-area-filter]");

    function filterProjects(tagQuery) {
      var selectedTags = tagQuery === "all" ? [] : tagQuery.split(/\s+/).filter(Boolean);
      var visibleCount = 0;

      filters.forEach(function (filter) {
        var isActive = filter.getAttribute("data-project-filter") === tagQuery;
        filter.classList.toggle("is-active", isActive);
        filter.setAttribute("aria-pressed", isActive ? "true" : "false");
      });

      rows.forEach(function (row) {
        var tagList = " " + (row.getAttribute("data-tags") || "") + " ";
        var isVisible = tagQuery === "all" || selectedTags.some(function (tag) {
          return tagList.indexOf(" " + tag + " ") !== -1;
        });
        row.hidden = !isVisible;
        if (isVisible) {
          visibleCount += 1;
        }
      });

      if (empty) {
        empty.hidden = visibleCount !== 0;
      }
    }

    filters.forEach(function (filter) {
      filter.addEventListener("click", function () {
        filterProjects(filter.getAttribute("data-project-filter"));
      });
    });

    areaCards.forEach(function (card) {
      function showAreaProjects() {
        activateView("projects");
        filterProjects(card.getAttribute("data-area-filter") || "all");
      }

      card.addEventListener("click", function (event) {
        if (event.target.closest("a")) {
          return;
        }
        showAreaProjects();
      });

      card.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          showAreaProjects();
        }
      });
    });

    var params = new URLSearchParams(window.location.search);
    var initialProjectTag = params.get("project-tag");

    if (window.location.hash === "#projects" || initialProjectTag) {
      activateView("projects");
    }

    if (initialProjectTag) {
      filterProjects(initialProjectTag);
    }
  }());
</script>
