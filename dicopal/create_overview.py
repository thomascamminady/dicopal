import altair as alt
import numpy as np
import polars as pl
from vega_datasets import data

alt.renderers.set_embed_options(actions=False)


def create_overview(
    palette: dict[str, list[str]]
) -> tuple[alt.HConcatChart, list[str]]:
    df = pl.DataFrame(
        [
            {"count": int(key), "color": color, "y": 1, "order": i}
            for key, colors in palette.items()
            for i, color in enumerate(colors)
        ]
    )

    colors = df["color"].unique().to_list()

    base = (
        alt.Chart(df)
        .encode(
            y=alt.Y("count:N").axis(None),
            order=alt.Order("order:Q"),
            tooltip=["color:N"],
        )
        .properties(
            width=900,
            height=30 * len(palette.items()),
        )
    )

    chart = (
        alt.hconcat(
            base.mark_bar().encode(
                x=alt.X("y:Q").axis(None).stack("zero"),
                color=alt.Color("color:N")
                .scale(range=colors, domain=colors)
                .legend(None),
            )
            # base.mark_text(fontSize=15, color="black").encode(
            #     x=alt.X("y:Q").axis(None).stack("zero"),
            #     text=alt.Text("color:N"),
            # ),
        )
        .configure_view(strokeWidth=0)
        .configure_axis(grid=False, domain=False)
    )

    colors = [
        ",".join(
            [
                f"'{str(c)}'"
                for c in df.filter(pl.col("count") == count)["color"].to_list()
            ]
        )
        for count in np.sort(df["count"].unique())
    ]

    return (chart, colors)


def create_example(palette):
    width = 180
    height = 150
    base = (
        alt.Chart(data.cars.url)
        .encode(color=alt.Color("Name:N").scale(range=palette).legend(None))
        .properties(width=width, height=height)
    )

    states = alt.topo_feature(data.us_10m.url, "states")
    source = data.population_engineers_hurricanes.url

    geomap = (
        alt.Chart(states)
        .mark_geoshape()
        .encode(alt.Color("engineers:N").scale(range=palette).legend(None))
        .transform_lookup(
            lookup="id", from_=alt.LookupData(source, "id", ["engineers"])
        )
        .properties(width=width, height=height)
        .project(type="albersUsa")
    )
    return (
        alt.vconcat(
            alt.hconcat(
                base.mark_circle(size=300, opacity=1).encode(
                    x=alt.X("Horsepower:Q").title(""),
                    y=alt.Y("Miles_per_Gallon:Q").title(""),
                ),
                base.mark_bar().encode(
                    x=alt.X("Miles_per_Gallon:Q").bin().title(""),
                    y=alt.Y("Miles_per_Gallon:Q").title(""),
                    color=alt.Color("Miles_per_Gallon:N")
                    .scale(range=palette)
                    .legend(None),
                ),
                base.mark_line(strokeWidth=4).encode(
                    x=alt.X("Horsepower:Q").title(""),
                    y=alt.Y("Miles_per_Gallon:Q").title(""),
                    color=alt.Color("Miles_per_Gallon:N")
                    .scale(range=palette)
                    .legend(None),
                ),
                geomap,
            ),
            # alt.hconcat(
            #     base.mark_line(strokeWidth=4).encode(
            #         x=alt.X("Horsepower:Q").title(""),
            #         y=alt.Y("Miles_per_Gallon:Q").title(""),
            #         color=alt.Color("Miles_per_Gallon:N")
            #         .scale(range=palette)
            #         .legend(None),
            #     ),
            #     geomap,
            # ),
        )
        .configure_view(strokeWidth=0)
        .configure_axis(grid=False, domain=False)
    )
