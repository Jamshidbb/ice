<script>
    import Frame from "./Frame.svelte";

    export let runs = [];
    export let selected;
    export let title;
    let index = 0;
    function set_index(i) {
        var keys = Object.keys(runs);
        index += i;
        if (index < 0) index = 0;
        else if (index == keys.length) index = keys.length - 1;
        selected = keys[index % keys.length];
    }
</script>

<Frame {title} cls="board" on:keydown={(e) =>
    set_index(e.code == "ArrowUp" ? -1 : e.code == "ArrowDown" ? 1 : 0)}>
    {#each Object.keys(runs) as run, i}
        <label class:selected={selected == run}>
            {run} ({runs[run]?.loss?.length})
            <button
                on:click={(e) => {
                    selected = run;
                    index = i;  
                }}>remove</button
            >
        </label>
    {/each}
</Frame>

<style>
    :global(.board) {
        overflow: auto;
        height: 100%;
        display: flex;
        grid-row: 1 / 3;
        grid-column: 1 / span 1;
        flex-direction: column;
        padding: 10px;
    }

    label {
        position: relative;
        line-height: 1.2;
        padding: 0.5em 2.5em 0.5em 2em;
        margin: 0 0 0.5em 0;
        border-radius: 2px;
        user-select: none;
        border: 1px solid hsl(240deg 32% 69%);
        background-color: hsl(240deg 100% 96%);
        color: #333;
        display: block;
    }

    button {
        position: absolute;
        top: 0;
        left: 0.2em;
        width: 2em;
        height: 100%;
        background: no-repeat 50% 50% url("../img/mark.svg");
        background-size: 1.4em 1.4em;
        border: none;
        opacity: 0;
        transition: opacity 0.2s;
        text-indent: -9999px;
        cursor: pointer;
    }

    label:hover button {
        opacity: 0.5;
    }

    label.selected button {
        opacity: 1;
    }
</style>
