import torch
import glob
import os
import re
import csv
from string import Template

points = False
samples = [0.1, 0.5, 1]
runs = [1, 4, 5, 6, 7]
loss_runs = [1, 5, 6]

fig_expriments_path = os.path.join('paper', 'fig', 'expriments', 'data')
fig_path = os.path.join('paper', 'fig', 'expriments', 'exp.tex')

fig_template = os.path.join('templates', 'fig.text')
with open(fig_template, 'r') as fig:
    template = fig.read()
    template = Template(template)
row_template = Template("$loss, $sigma, $run$stepn.csv, $step")
rows = []

fig_losses_path = os.path.join('paper', 'fig', 'losses', 'data')
fig_loss_path = os.path.join('paper', 'fig', 'losses', 'losses.tex')
fig_loss_template = os.path.join('templates', 'loss.text')
with open(fig_loss_template, 'r') as fig:
    fig_loss_template = fig.read()
    fig_loss_template = Template(fig_loss_template)
loss_row_template = Template("$loss, $sigma, $run")
loss_rows = []

def props(name):
    name = os.path.basename(name)
    res = re.match(
        'expriment_(?P<loss>[A-Z]*)_sigma_(?P<d1>[\d]*)_(?P<d2>[\d]*)?[_]?\d{8}_\d{6}.pt',
        name
    )
    sigma = res.group('d1')
    if res.group('d2'):
        sigma += '.' + res.group('d2')
    return res.group('loss'), sigma

def tocsv(path, run_step):
    keys = run_step[0].keys()
    with open(path, 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(run_step)

run_index = 0

for f in glob.glob(os.path.join(os.getcwd(), 'logs', '*.pt')):
    run_index += 1
    if run_index not in runs:
        continue
    with open(f, 'r') as file:
        loss, sigma = props(file.name)
        run = torch.load(f)

        if not points:
            tocsv(
                os.path.join(fig_expriments_path, 'points.csv'),
                run['points']
            )
            points = True
        if run_index in loss_runs:
            tocsv(
                os.path.join(fig_losses_path, f'mseloss_{run_index}.csv'),
                [{'x':x, 'y':y} for x,  y in zip(run['steps'], run['loss'])]
            )
            tocsv(
                os.path.join(fig_losses_path, f'iceloss_{run_index}.csv'),
                [{'x':x, 'y':y} for x,  y in zip(run['steps'], run['netloss'])]
            )
            loss_rows.append(loss_row_template.substitute({
                'loss': loss,
                'sigma': sigma,
                'run': run_index
            }))

        pred = run['pred']
        total = run['total']
        steps = run['steps']
        for s in [x * total for x in samples]:
            index, step = min(enumerate(steps), key=lambda x: abs(x[1]-s))
            csvpath = os.path.join(fig_expriments_path, f'{run_index}_{step}.csv')
            tocsv(csvpath, pred[index])
            row = row_template.substitute({
                'loss': loss,
                'sigma': sigma,
                'run': str(run_index) + '_',
                'step': step + 1,
                'stepn': step
            })
            rows.append(row)

template = template.substitute({
    'rows': "\n\t".join(rows),
    'columns': len(samples),
    'rows_count': len(runs),
    'length': len(samples) * len(runs) -  1
})

with open(fig_path, 'w') as fig:
    fig.write(template)

fig_loss_template = fig_loss_template.substitute({
    'rows': "\n\t".join(loss_rows),
    'columns': 2,
    'rows_count': len(loss_runs),
    'length': len(loss_runs) - 1
})

with open(fig_loss_path, 'w') as fig:
    fig.write(fig_loss_template)