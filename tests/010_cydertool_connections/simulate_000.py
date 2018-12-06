# coding: utf-8
import pandas
from pyfmi import load_fmu
from pyfmi.fmi_coupled import CoupledFMUModelME2
import datetime as dt
import json
from lxml import etree
import shlex, subprocess

# Read FMU structure
fmu_path = 'pandapower/'
df = pandas.read_excel(fmu_path + 'pandapower.xlsx')
model_name = 'pandapower'

# Create the XML file
NSMAP = {"xsi" : 'http://www.w3.org/2001/XMLSchema-instance'}
root = etree.Element("SimulatorModelDescription", nsmap={'xsi': NSMAP['xsi']})
root.set("fmiVersion", "2.0")
root.set("modelName", model_name)
root.set("description", model_name)
root.set("generationTool", "SimulatorToFMU")
model_variables = etree.SubElement(root, "ModelVariables")
for index, row in df.iterrows():
    variable = etree.SubElement(model_variables, "ScalarVariable")
    variable.set("name", row['name'])
    variable.set("description", row['description'])
    variable.set("causality", row['causality'])
    variable.set("start", str(row['start']))
    variable.set("type", row['type'])
    variable.set("unit", row['unit'])
my_tree = etree.ElementTree(root)
with open(fmu_path + 'model_description.xml', 'wb') as f:
    f.write(etree.tostring(my_tree, xml_declaration=True,
                           encoding='UTF-8'))

# Compile the FMU
cmd = ("python C:/Users/DRRC/Desktop/desktops/February/SimulatorToFMU" +
       "/simulatortofmu/parser/SimulatorToFMU.py " +
       "-i " + fmu_path + 'model_description.xml' + " -s "  + fmu_path +
       model_name + "_wrapper.py " +
       "-x python -t jmodelica -pt C:/JModelica.org-2.1 " + "-a me")
args = shlex.split(cmd)
process = subprocess.Popen(args)
process.wait()

# Read simulation inputs
df = pandas.read_excel('connections.xlsx')
start = dt.datetime(2018, 6, 17, 3, 0, 0)
end = dt.datetime(2018, 6, 17, 22, 5, 0)
begin = dt.datetime(2018, 1, 1, 0, 0, 0)
start_s = int((start - begin).total_seconds())
end_s = int((end - begin).total_seconds())
print('Start: ' + str(start_s) + ' seconds')
print('End: ' + str(end_s) + ' seconds')

# Create a list of unique FMUs
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
print(fmus)

# Load FMUs and set parameters
fmus['fmu'] = [None] * len(fmus)
fmus['name'] = [None] * len(fmus)
models =[]
for index, row in fmus.iterrows():
    fmus.loc[index, 'name'] = str(row['id'])
    fmus.loc[index, 'fmu'] = (load_fmu(
      row['path'], log_level=7))
    fmus.loc[index, 'fmu'].setup_experiment(
      start_time=start_s, stop_time=end_s)
    for key, value in row['parameter'].items():
        fmus.loc[index, 'fmu'].set(key, value)
    models.append((fmus.loc[index, 'name'],
                   fmus.loc[index, 'fmu']))

# Create connection list
connections = []
variables = []
for index, row in df.iterrows():
    connections.append((fmus[fmus['id'] == row['fmu1_id']]['fmu'].iloc[0],
                        row['fmu1_output'],
                        fmus[fmus['id'] == row['fmu2_id']]['fmu'].iloc[0],
                        row['fmu2_input']))

    # Save variable names to retrive later
    variables.append(str(fmus[fmus['id'] == row['fmu1_id']]['name'].iloc[0]) +
                     '.' + row['fmu1_output'])
    variables.append(str(fmus[fmus['id'] == row['fmu2_id']]['name'].iloc[0]) +
                     '.' + row['fmu2_input'])

# Create master and run simulation
master = CoupledFMUModelME2(models, connections)
options = master.simulate_options()
print(options)
import pdb
pdb.set_trace()
options['ncp'] = 500
pyfmi_results = master.simulate(options=options,
    start_time=start_s, final_time=end_s)

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
print('Done')
