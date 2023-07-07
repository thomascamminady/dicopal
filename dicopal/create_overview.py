import altair as alt
import polars as pl


def create_overview(palette: dict[str, list[str]]) -> tuple[alt.HConcatChart, str]:
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
            width=600,
            height=300,
        )
    )

    chart = (
        alt.hconcat(
            base.mark_bar().encode(
                x=alt.X("y:Q").axis(None).stack("normalize"),
                color=alt.Color("color:N")
                .scale(range=colors, domain=colors)
                .legend(None),
            ),
            # base.mark_text(fontSize=15, color="black").encode(
            #     x=alt.X("y:Q").axis(None).stack("zero"),
            #     text=alt.Text("color:N"),
            # ),
        )
        .configure_view(strokeWidth=0)
        .configure_axis(grid=False, domain=False)
    )
    colors = ",".join(
        [
            f"'{str(c)}'"
            for c in df.filter(pl.col("count") == df["count"].max())["color"].to_list()
        ]
    )

    return (chart, colors)
