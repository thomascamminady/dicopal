import json

from IPython.core.display import Markdown
from IPython.display import display

from dicopal.create_overview import create_example, create_overview


def create(palettes, source, palette, url, palettetype, include_example):
    chart, colors = create_overview(palettes[source][palette]["values"])

    n = len(colors) // 5
    colorhex = [c.strip("'") for c in colors[n].split(",")]
    example = create_example(colorhex)
    display(Markdown(f"   \n## [{palette}]({url}), {palettetype}"))
    color_strings = [f"\n[{color}]" for color in colors]
    color_string = "".join(color_strings)
    display(chart)

    display(Markdown(f"""```python{color_string}\n```"""))
    color_strings = [f"\n[{color}]" for color in colors[n : n + 1]]
    color_string = "".join(color_strings)
    if include_example:
        display(Markdown("Here are some example plots."))
        display(example)
        display(
            Markdown(
                f"""Specifically, the following colors where used for the example.\n```python{color_string}\n```"""
            )
        )
    # display(Markdown("```python\n[\n " + ",\n ".join(colors.split(",")) + ",\n]\n```"))


def create_page(
    source: str,
    path: str = "../dicopal.js/src/palettes_apdocc.json",
    include_example=True,
):
    with open(path, "r") as f:
        palettes = json.load(f)

    for palette in palettes[source].keys():
        palettetype = palettes[source][palette]["type"]
        url = palettes[source][palette]["url"]
        create(palettes, source, palette, url, palettetype, include_example)


def create_page_by_type(
    requested_palettetype: str,
    path: str = "../dicopal.js/src/palettes_apdocc.json",
    include_example=True,
):
    with open(path, "r") as f:
        palettes = json.load(f)

    for source in palettes.keys():
        for palette in palettes[source].keys():
            palettetype = palettes[source][palette]["type"]
            if requested_palettetype == palettetype:
                url = palettes[source][palette]["url"]
                create(palettes, source, palette, url, palettetype, include_example)
