# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal academic/professional website for Milan Jain (Senior Research Scientist at PNNL), built with Jekyll and the [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes) theme, hosted on GitHub Pages at `https://jainmilan.github.io`.

## Common Commands

```bash
# Serve locally with live reload (primary dev command)
bundle exec jekyll serve

# Build static site to _site/
bundle exec jekyll build

# Update Ruby gems (run after long periods of inactivity)
bundle update

# Check Jekyll version
bundle exec jekyll -v
```

After any changes, deploy with:
```bash
git commit -a -m "<message>" && git push
```

## Architecture

The site uses the `mmistakes/minimal-mistakes@4.26.2` remote theme — most layout, include, and SCSS files in the repo are **overrides** of theme defaults. When editing `_layouts/`, `_includes/`, or `_sass/`, check the [upstream theme source](https://github.com/mmistakes/minimal-mistakes) to understand the base behavior before modifying.

**Key configuration** lives in `_config.yml` — changes here require restarting `jekyll serve` to take effect (unlike content changes, which hot-reload).

**Content structure:**
- `_posts/` — Blog posts, filename format `YYYY-MM-DD-slug.md`
- `_pages/` — Static pages (`about.md` is the home page at `/`, `publications.md`, `research.md`, `cv.md`, `posts.md`)
- `_data/navigation.yml` — Controls the top nav menu items
- `assets/images/` — Images, including `milan.jpg` (author avatar)

## Blog Post Front Matter

```yaml
---
title: "Post Title"
excerpt_separator: <!--more-->
category:
    - technical   # or: opinion, research
tags:
    - tag1
    - tag2
---
```

Posts default to `layout: single`, author profile sidebar, read-time estimate, comments enabled, and related posts enabled (set in `_config.yml` defaults). MathJax is enabled via Kramdown — use standard LaTeX delimiters for equations.

## Theme Customization Notes

- `minimal_mistakes_skin` in `_config.yml` controls the color skin (`"default"` currently; options: `air`, `aqua`, `contrast`, `dark`, `dirt`, `neon`, `mint`, `plum`, `sunrise`)
- Sass source is in `_sass/minimal-mistakes/` — compiled output goes to `assets/css/main.css`
- The `_site/` directory is the generated output; never edit it directly
- Comments provider is not currently configured (`provider:` is blank in `_config.yml`)
