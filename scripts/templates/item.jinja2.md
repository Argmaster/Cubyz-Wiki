---
icon: material/{%- if zon["material"] -%} alpha-m-box-outline {%- else -%} alpha-i-box-outline {%- endif %}
---

# {{ name }}

!!! infobox "{{ name }}"

    ![Image title]({{ cfg.image_root }}/{{ relative_to_source_no_suffix.with_suffix(".png").as_posix() }}){ width="300" align=left }

    | | |
    |:-|-:|
    |**ID**| {{ id }} |
{%- if zon["tags"] %}
    |**Tags**| {% for tag in zon["tags"]|sort %} {{ tag }}{% if not loop.last %},{% endif %} {% endfor %} |
{%- endif -%}
{%- if zon["material"] %}
    |**Durability**| {{ zon["material"]["durability"] }} |
    |**Mass Damage**| {{ zon["material"]["massDamage"] }} |
    |**Hardness Damage**| {{ zon["material"]["hardnessDamage"] }} |
    |**Swing Speed**| {{ zon["material"]["swingSpeed"] }} |
{%- endif %}

## About

> This section is a stub. You can help the Cubyz Wiki by expanding it.

## Obtaining

> This section is a stub. You can help the Cubyz Wiki by expanding it.

## Usage

> This section is a stub. You can help the Cubyz Wiki by expanding it.

## History

> This section is a stub. You can help the Cubyz Wiki by expanding it.
