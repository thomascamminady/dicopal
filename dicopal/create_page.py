import json

from IPython.core.display import Markdown
from IPython.display import display

from dicopal.create_overview import create_overview


def create_page(source: str):
    with open("../dicopal.js/src/palettes.json", "r") as f:
        palettes = json.load(f)

    for palette in palettes[source].keys():
        chart, colors = create_overview(palettes[source][palette]["values"])
        palettetype = palettes[source][palette]["type"]
        url = palettes[source][palette]["url"]
        display(Markdown(f"## [{palette}]({url}), {palettetype}"))
        display(chart)
        display(Markdown("```[" + colors + "]```"))
