from aiida import load_profile
from aiida.orm import StructureData
from ase.build import bulk
from ase.io import read
from aiida_mlip.data.model import ModelData
from aiida.orm import load_code
from aiida.orm import Str
from aiida.plugins import CalculationFactory
from aiida.engine import run_get_node

load_profile()

structure = StructureData(ase=bulk("NaCl", "rocksalt", 5.63))
uri = "https://github.com/stfc/janus-core/raw/main/tests/models/mace_mp_small.model"
model = ModelData.from_uri(uri, architecture="mace_mp", cache_dir="mlips")

code = load_code("janus@localhost")

inputs = {
    "metadata": {"options": {"resources": {"num_machines": 1}}},
    "code": code,
    "arch": model.architecture,
    "struct": structure,
    "model": model,
    "device": Str("cpu"),
}

singlepointCalc = CalculationFactory("mlip.sp")

result, node = run_get_node(singlepointCalc, inputs)

print(result)
print(node)