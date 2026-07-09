---
icon: material/
{%- if "mineable" in zon["tags"] -%} pickaxe
{%- elif "choppable" in zon["tags"] -%} axe
{%- elif "diggable" in zon["tags"] -%} shovel
{%- elif "cuttable" in zon["tags"] -%} sickle
{%- elif "fluid" in zon["tags"] -%} water
{%- else -%} box-shadow {%- endif %}
---

# {{ name }}

!!! infobox "{{ name }}"

    {% if zon["texture"] -%}
    {%- elif zon["texture"] -%}
    ![Image title]({{ cfg.image_root }}/{{ extract_texture_relpath(zon["texture"]) }}){ width="300" align=left }
    {%- elif zon["texture0"] -%}
    ![Image title]({{ cfg.image_root }}/{{ extract_texture_relpath(zon["texture0"]) }}){ width="300" align=left }
    {%- else -%}
    ![Image title]({{ cfg.image_root }}/{{ relative_to_source_no_suffix.with_suffix(".png").as_posix() }}){ width="300" align=left }
    {%- endif %}

    | | |
    |:-|-:|
    |**ID**| {{ id }} |
    |**Block Health**| {{ zon["blockHealth"] }} |
{%- if zon["ore"] %}
    |**Max Height**| {{ zon["ore"]["maxHeight"] }} |
    |**Min Height**| {{ zon["ore"]["minHeight"] }} |
{%- endif %}


{% if zon["item"] -%}
{%- if zon["item"]["material"] %}
    | | |
    |:-|-:|
    |**Durability**| {{ zon["item"]["material"]["durability"] }} |
    |**Mass Damage**| {{ zon["item"]["material"]["massDamage"] }} |
    |**Hardness Damage**| {{ zon["item"]["material"]["hardnessDamage"] }} |
    |**Swing Speed**| {{ zon["item"]["material"]["swingSpeed"] }} |
{%- endif -%}
{%- endif %}


{%  if zon["tags"] %}
    {% for tag in zon["tags"]|sort %} <span class="md-tag md-tag-icon"> {{ tag }} </span> {% endfor %}
{%- endif %}

## About

> This section is a stub. You can help the Cubyz Wiki by expanding it.

## Obtaining

> This section is a stub. You can help the Cubyz Wiki by expanding it.

## Usage

> This section is a stub. You can help the Cubyz Wiki by expanding it.

## History

> This section is a stub. You can help the Cubyz Wiki by expanding it.
