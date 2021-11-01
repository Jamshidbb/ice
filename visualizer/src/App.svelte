<script>
	import FittingChart from "./components/FittingChart.svelte";
	import LossChart from "./components/LossChart.svelte";
	import Runs from "./components/Runs.svelte";
	import Progress from "./components/Progress.svelte";

	let insertAt = (arr, index, value) => {
		if (!arr) return [value];
		return [...arr.slice(0, index), value, ...arr.slice(index, -1)];
	};

	let run;
	let runs = {};
	let ws = new WebSocket("ws://127.0.0.1:8765/");

	ws.onmessage = (event) => {
		let data = JSON.parse(event.data);
		// console.log(data);
		if (data.run == "...") {
			runs = data.value;
			run = Object.keys(runs)[0];
			return;
		} else {
			if (!run) run = data.run;
			if (!runs[data.run]) {
				runs[data.run] = {};
				run = data.run;
			}

			runs = {
				...runs,
				[data.run]: {
					...runs[data.run],
					[data.key]: data.isArray
						? insertAt(
								runs[data.run][data.key],
								data.step,
								data.value
						  )
						: data.value,
					step: data.step,
				},
			};
		}
	};
</script>

<div class="container grid grid-simple-col-4">
	<div id="chart-01" class="main section">
		<FittingChart
			pred={runs[run]?.pred?.at(-1)}
			points={runs[run]?.points}
		/>
	</div>
	<div id="runs" class="section">
		<Runs {runs} title="Runs" bind:selected={run} />
	</div>
	<div id="loss" class="section">
		<LossChart losses={runs[run]?.loss} />
	</div>
	<div id="netloss" class="section">
		<LossChart title="net loss" losses={runs[run]?.netloss} />
	</div>
	<div id="progress" class="section">
		<Progress total={runs[run]?.total} sofar={runs[run]?.step + 1} />
	</div>
</div>

<style>
	.section {
		min-width: 0;
		height: 100%;
		margin-bottom: 1rem;
	}
	.main.section {
		grid-column: 1 / span 1;
		grid-row: 1 / 2;
	}
	#runs {
		height: 350px;
		grid-column: 1 / span 1;
		grid-row: 2 / 3;
	}
	#loss {
		grid-column: 1 / span 1;
		grid-row: 3 / 4;
	}
	#netloss {
		grid-column: 1 / span 1;
		grid-row: 4 / 5;
	}
	#progress {
		grid-column: 1 / span 1;
		grid-row: 5 / 6;
	}

	@media (min-width: 768px) {
		.section {
			margin-bottom: 0;
		}

		.main.section {
			grid-column: 2 / span 3;
			grid-row: 1 / 6;
		}
		#netloss {
			grid-row: 2 / 4;
			grid-column: 1 / span 1;
		}
		#loss {
			grid-row: 4 / 6;
			grid-column: 1 / span 1;
		}
		#progress {
			grid-row: 6 / 6;
			grid-column: 1 / span 4;
		}
		#runs {
			height: 350px;
			grid-row: 1 / 2;
			grid-column: 1 / span 1;
		}
	}
</style>
