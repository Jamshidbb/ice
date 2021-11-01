<script>
    import * as d3 from "d3";
    import * as fc from "d3fc";
    import Frame from "./Frame.svelte";

    export let title = "Loss";
    export let losses = [];
    let ctx;
    let chart;
    let xScale;
    let yScale;
    const extent = fc.extentLinear().pad([0.02, 0]);

    let render = () => {
        ctx ? d3.select(ctx).datum(losses).call(chart) : null;
    };

    $: {
        if (losses) {
            if (ctx && losses?.length > 0 && !chart) {
                xScale = d3.scaleLinear().domain([0, losses.length - 1]);
                yScale = d3.scaleLinear().domain(extent(losses));
                const series = fc
                    .seriesWebglLine()
                    .xScale(xScale)
                    .yScale(yScale)
                    .crossValue((_, i) => i)
                    .mainValue((d) => d)
                    .decorate((program) => {
                        fc
                            .webglStrokeColor()
                            .data(losses)
                            .value((d) => [65 / 255, 26 / 255, 196 / 255, 1.0])(
                            program
                        );
                    });
                const zoom = fc.zoom().on("zoom", (event) => render());
                chart = fc
                    .chartCartesian(xScale, yScale)
                    .webglPlotArea(series)
                    .decorate((sel) => {
                        sel.enter().call(zoom, xScale, yScale);
                    });
            }
            xScale?.domain([0, losses.length - 1]);
            yScale?.domain(extent(losses));
            if (chart) render();
        }
    }
</script>

<Frame {title}>
    <div id="chart" bind:this={ctx} />
</Frame>

<style>
    #chart {
        margin: auto;
        height: 100%;
        width: 100%;
    }
</style>
