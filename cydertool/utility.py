# coding: utf-8
import pandas
from pyfmi import load_fmu
from pyfmi.fmi_coupled import CoupledFMUModelME2
import datetime as dt
import json
from lxml import etree
import shlex, subprocess

# Compile FMU
def compile(path, name, fmu_type='me', fmu_struc='python',
            path_to_simulatortofmu=(
            'C:/Users/DRRC/Desktop/desktops/February/SimulatorToFMU' +
            '/simulatortofmu/parser/SimulatorToFMU.py')):
    """
    1) Create an XML model description from Excel file
    2) Compile the FMU using SimulatorToFMU
    """
    # Create the XML
    structure = pandas.read_excel(path + 'structure.xlsx')
    NSMAP = {"xsi" : 'http://www.w3.org/2001/XMLSchema-instance'}
    root = etree.Element("SimulatorModelDescription",
                         nsmap={'xsi': NSMAP['xsi']})
    root.set("fmiVersion", "2.0")
    root.set("modelName", name)
    root.set("description", name)
    root.set("generationTool", "SimulatorToFMU")
    model_variables = etree.SubElement(root, "ModelVariables")
    for index, row in structure.iterrows():
        variable = etree.SubElement(model_variables, "ScalarVariable")
        variable.set("name", row['name'])
        variable.set("description", row['description'])
        variable.set("causality", row['causality'])
        variable.set("start", str(row['start']))
        variable.set("type", row['type'])
        variable.set("unit", row['unit'])
    my_tree = etree.ElementTree(root)
    with open(path + 'model_description.xml', 'wb') as f:
        f.write(etree.tostring(my_tree, xml_declaration=True,
                               encoding='UTF-8'))

    # Compile the FMU
    cmd = ("python " + path_to_simulatortofmu +
           " -i " + fmu_path + 'model_description.xml' +
           " -s " + fmu_path + model_name + "_wrapper.py" +
           " -x " + fmu_struc +
           " -t jmodelica" +
           " -pt C:/JModelica.org-2.1" +
           " -a " + fmu_type)
    args = shlex.split(cmd)
    process = subprocess.Popen(args)
    process.wait()
    return True

# Load FMUs, connect them and launch the simulation
def simulate(start, end, connections, me=True, nb_steps=500):
    """
    1) Load and parametrize unique FMUs
    2) Connect FMUs through the Master
    3) Launch the simulation
    4) Save all the variables to a CSV file
    """
    # Create a list of unique FMUs
    df = pandas.read_excel(connections)
    fmu_ids = df['fmu1_id'].tolist()
    fmu_ids.extend(df['fmu2_id'].tolist())
    fmu_paths = df['fmu1_path'].tolist()
    fmu_paths.extend(df['fmu2_path'].tolist())
    fmu_parameters = df['fmu1_parameters'].tolist()
    fmu_parameters.extend(df['fmu2_parameters'].tolist())
    fmus = pandas.DataFrame(data={'id': fmu_ids,
                                  'path': fmu_paths,
                                  'parameter': fmu_parameters})
    fmus = fmus.drop_duplicates(['id'])
    fmus['parameter'] = fmus['parameter'].apply(lambda x: json.loads(x))

    # Load FMUs and set parameters
    fmus['fmu'] = [None] * len(fmus)
    fmus['name'] = [None] * len(fmus)
    models =[]
    for index, row in fmus.iterrows():
        fmus.loc[index, 'name'] = str(row['id'])
        fmus.loc[index, 'fmu'] = (load_fmu(
          row['path'], log_level=7))
        fmus.loc[index, 'fmu'].setup_experiment(
          start_time=start, stop_time=end)
        for key, value in row['parameter'].items():
            fmus.loc[index, 'fmu'].set(key, value)
        models.append((fmus.loc[index, 'name'],
                       fmus.loc[index, 'fmu']))

    # Create connection list
    connections = []
    variables = []
    for index, row in df.iterrows():
        connections.append(
            (fmus[fmus['id'] == row['fmu1_id']]['fmu'].iloc[0],
             row['fmu1_output'],
             fmus[fmus['id'] == row['fmu2_id']]['fmu'].iloc[0],
             row['fmu2_input']))

        # Save variable names to retrive later
        variables.append(
            str(fmus[fmus['id'] == row['fmu1_id']]['name'].iloc[0]) +
            '.' + row['fmu1_output'])
        variables.append(
            str(fmus[fmus['id'] == row['fmu2_id']]['name'].iloc[0]) +
            '.' + row['fmu2_input'])

    # Create master and run simulation
    master = CoupledFMUModelME2(models, connections)
    options = master.simulate_options()
    options['ncp'] = nb_steps
    pyfmi_results = master.simulate(options=options,
        start_time=start, final_time=end)

    # Terminate FMUs
    for index, row in fmus.iterrows():
        fmus.loc[index, 'fmu'].terminate()

    # Retrieve results and save
    results = pandas.DataFrame(
        index=pyfmi_results['time'],
        data={key: pyfmi_results[key]
              for key in variables})
    results.index.name = 'time'
    results.to_csv('results.csv')
    return results
