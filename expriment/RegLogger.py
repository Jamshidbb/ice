import os
from pathlib import Path
import torch
from logserver.MemoryLogServer import MemoryLogServer

class RegLogger(MemoryLogServer):
    def __init__(self, logroot, delay=0.01, port=4444, wsport=8765, *args, **kwargs):
        super().__init__(logroot, delay=delay, port=port, wsport=8765, *args, **kwargs)
        self.loaded = False
        self.runs = None
        self.start()

    def log(self, key, value, step = None):
        if not self.runs:
            self.runs = {self.run_name:{'steps':[]}}
        if not self.run_name in self.runs:
            self.runs[self.run_name] = {'steps':[]}
        isArray =  False
        if key == "total" or key == "points":
            self.runs[self.run_name][key] = value
        else:
            if not key in self.runs[self.run_name]:
                self.runs[self.run_name][key] = []
            isArray = True
            self.runs[self.run_name][key].insert(step, value)
        
        self.runs[self.run_name]["step"] = step
        
        if step is not None and step not in self.runs[self.run_name]["steps"]:
            self.runs[self.run_name]["steps"].append(step)
        
        super().put({"run": self.run_name, "isArray": isArray, "step":step, "key":key, "value": value})

    def start(self):
        super().start()

    def init(self):
        return {"run": "...", "value": self.runs}

    def save(self):
        name = os.path.join(self.logroot, f'{self.run_name}.pt')
        torch.save(self.runs[self.run_name], name)
        print(f'{self.run_name} saved')

    def load(self):
        if self.loaded:
            return
        for f in Path(self.logroot).rglob('*.pt'):
            name = os.path.splitext(f)[0].split('/')[-1]
            run = torch.load(f)
            self.runs[name] = run
        self.loaded = True
            
