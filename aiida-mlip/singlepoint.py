from aiida import load_profile
from aiida.orm import StructureData, Str, load_code, Dict, SinglefileData
from ase.io import read
from aiida_mlip.data.model import ModelData
from aiida.plugins import CalculationFactory
from aiida.engine import run_get_node
from pathlib import Path

import os
import shutil
import yaml

OUTPUT_FOLDER= Path("/app/outputs")


def run_singlepoint(structure_path: Path):
    load_profile()

    structure = StructureData(ase=read(structure_path))
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

    return result, node

def calculation_output_file(results_dict: Dict, xyz_output: SinglefileData):

    with xyz_output.open(mode='rb') as source:
        with open(f"{OUTPUT_FOLDER}/structure.xyz", mode='wb') as target:
            shutil.copyfileobj(source, target)
    
    with open(f"{OUTPUT_FOLDER}/results_dict.yaml", mode='w') as target:
        yaml.dump(results_dict.get_dict(), target)


def main():

    inputs = os.listdir('aiida-mlip/inputs')
    print("inputs", inputs)

    input_structure = 'aiida-mlip/inputs/' + inputs[0]

    result, node = run_singlepoint(Path(input_structure))

    print(result['results_dict'])
    print(result['xyz_output'])

    calculation_output_file(result['results_dict'], result['xyz_output'])


if __name__ == "__main__":
    main()

    

