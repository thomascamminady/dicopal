import json

from IPython.core.display import Markdown
from IPython.display import display

from dicopal.create_overview import create_overview


def create_page(source: str, path: str = "../dicopal.js/src/palettes.json"):
    with open(path, "r") as f:
        palettes = json.load(f)

    for palette in palettes[source].keys():
        chart, colors = create_overview(palettes[source][palette]["values"])
        palettetype = palettes[source][palette]["type"]
        url = palettes[source][palette]["url"]
        display(Markdown(f"## [{palette}]({url}), {palettetype}"))
        display(chart)
        display(Markdown("```[" + colors + "]```"))


def create_page_by_type(
    requested_palettetype: str, path: str = "../dicopal.js/src/palettes.json"
):
    with open(path, "r") as f:
        palettes = json.load(f)

    for source in palettes.keys():
        for palette in palettes[source].keys():
            palettetype = palettes[source][palette]["type"]
            if requested_palettetype == palettetype:
                chart, colors = create_overview(palettes[source][palette]["values"])
                url = palettes[source][palette]["url"]
                display(Markdown(f"## [{palette}]({url}), {palettetype}"))
                display(chart)
                display(Markdown("```[" + colors + "]```"))
