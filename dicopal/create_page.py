import json

from IPython.core.display import Markdown
from IPython.display import display

from dicopal.create_overview import create_overview


def create(palettes, source, palette, url, palettetype):
    chart, colors = create_overview(palettes[source][palette]["values"])
    display(Markdown(f"## [{palette}]({url}), {palettetype}"))
    color_strings = [f"\n[{color}]" for color in colors]
    color_string = "".join(color_strings)
    display(chart)
    display(Markdown(f"""```python{color_string}\n```"""))
    # display(Markdown("```python\n[\n " + ",\n ".join(colors.split(",")) + ",\n]\n```"))


def create_page(source: str, path: str = "../dicopal.js/src/palettes_apdocc.json"):
    with open(path, "r") as f:
        palettes = json.load(f)

    for palette in palettes[source].keys():
        palettetype = palettes[source][palette]["type"]
        url = palettes[source][palette]["url"]
        create(palettes, source, palette, url, palettetype)


def create_page_by_type(
    requested_palettetype: str, path: str = "../dicopal.js/src/palettes_apdocc.json"
):
    with open(path, "r") as f:
        palettes = json.load(f)

    for source in palettes.keys():
        for palette in palettes[source].keys():
            palettetype = palettes[source][palette]["type"]
            if requested_palettetype == palettetype:
                url = palettes[source][palette]["url"]
                create(palettes, source, palette, url, palettetype)
