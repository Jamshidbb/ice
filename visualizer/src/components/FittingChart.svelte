<script>
    import * as d3 from "d3";
    import * as fc from "d3fc";
    import { onMount } from "svelte";
    import Frame from "./Frame.svelte";
    export let points;
    export let pred;

    let data = [];
    let ctx;
    const xScale = d3.scaleLinear().domain([0, data.length - 1]);

    const yScale = d3
        .scaleLinear()
        .domain(fc.extentLinear().pad([0.5, 0.5])(data));

    onMount(async () => render());

    const x = d3.scaleLinear().domain([-1.1, 1.1]);
    const y = d3.scaleLinear().domain([-1.5, 5]);

    const pointSeries = fc
        .seriesWebglPoint()
        .type(d3.symbolCircle)
        .crossValue((d) => d.x)
        .mainValue((d) => d.y)
        .decorate((program) => {
            fc.webglFillColor([0, 0, 1, 0.4])(program);
            fc
                .webglStrokeColor()
                .data(data)
                .value((d) => [0, 0, 1, 1.0])(program);
        });

    const lineSeries = fc
        .seriesWebglLine()
        .crossValue((d) => d.x)
        .mainValue((d) => d.z)
        .decorate((program) => {
            fc
                .webglStrokeColor()
                .data(data)
                .value((d) => [1, 0, 0, 1.0])(program);
        });

    let combind = fc
        .seriesWebglMulti()
        .xScale(xScale)
        .yScale(yScale)
        .series([lineSeries, pointSeries]);

    const zoom = fc.zoom().on("zoom", (event) => render());

    const chart = fc
        .chartCartesian(x, y)
        .xLabel("X")
        .yLabel("Y")
        .webglPlotArea(combind)
        .decorate((sel) => {
            sel.enter().call(zoom, x, y);
        });

    const render = () => {
        d3.select(ctx).datum(data).call(chart);
    };

    $: {
        if (!!pred) {
            rerender();
        }
    }

    function rerender() {
        data = points?.map((item, i) => ({
            ...item,
            z: pred.find((p) => p.x === item.x)?.y,
        }));
        data = data ? data : [];
        render();
    }
</script>

<Frame title="data">
    <div class="fill-box" id="chart" bind:this={ctx} />
</Frame>

<style>
    .fill-box {
        margin: auto;
        height: 100%;
        width: 100%;
    }
</style>
