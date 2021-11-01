<script>
    import { tweened } from "svelte/motion";
    import { cubicOut } from "svelte/easing";

    export let sofar = 0;
    export let total = 1;

    const value = tweened(0.0, {
        duration: 400,
        easing: cubicOut,
    });

    $: {
        if (!isNaN(sofar)) {
            $value = Math.round(((100 * sofar) / total) * 100) / 100;
        }
    }
</script>

<div class="progress">
    <div class="progress-bar-text">{$value.toFixed(0)}%</div>
    <div class="progress-bar" style="width: {$value.toFixed(0)}%;" />
</div>

<style>
    .progress {
        width: 100%;
        display: inline-block;
        overflow: hidden;
        height: 28px;
        background-color: #ddd;
        border-radius: 4px;
        position: relative;

        display: flex;
        justify-content: center;
        flex-direction: column;
    }

    .progress-bar-text {
        position: absolute;
        left: 50%;
        font-style: italic;
        font-size: 1em;
        transform: translateX(-50%);
        font-family: Tahoma, helvetica, arial, sans-serif;
    }

    .progress-bar {
        width: 0;
        border-radius: 4px;
        height: 100%;
        font-size: 14px;
        line-height: 22px;
        color: #464e5b;
        text-align: center;
        background-color: #61d265;
    }

    .button {
        padding: 8px;
        background-color: #d2d2d2;
        height: 100%;
        text-align: center;
        text-decoration: none;
        color: black;

        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;

        border-radius: 15px;
        cursor: pointer;
    }

    .button.medium {
        height: 18px;
        width: 80px;
    }

    .button:hover {
        background-color: #bdbdbd;
    }

    .inline {
        display: inline-block;
    }

    .main {
        text-align: center;
        margin-left: auto;
        margin-right: auto;
    }
</style>
