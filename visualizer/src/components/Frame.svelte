<script>
    export let title = "";
    export let cls = "";
</script>

<div class="box">
    <div class="box-title">{title}</div>
    <div class="{cls} box-body">
        <slot />
    </div>
</div>

<style>
    .box {
        height: 100%;
        background: #fff;
        border: 1px solid #e7e7e7;
        border-radius: 2px;
        box-sizing: border-box;
        padding-bottom: 25px;
        padding-right: 4px;
    }

    .box-title {
        border-bottom: 1px solid #e7e7e7;
        border-radius: 2px 2px 0 0;
        font-size: 13px;
        padding: 2px 10px 0;
        text-transform: uppercase;
    }

    .box-body {
        margin: auto;
        height: 100%;
        width: 100%;
    }

    ::-webkit-scrollbar {
        width: 20px;
    }

    ::-webkit-scrollbar-track {
        background-color: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background-color: #d6dee1;
        border-radius: 20px;
        border: 6px solid transparent;
        background-clip: content-box;
    }

    ::-webkit-scrollbar-thumb:hover {
        background-color: #a8bbbf;
    }
</style>
