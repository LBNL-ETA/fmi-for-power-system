# coding: utf-8
import click
import pandas
from lxml import etree
import shlex, subprocess

# Compile FMU
@click.command()
@click.option('--path', required=True, type=str)
@click.option('--name', required=True, type=str)
@click.option('--type', required=False, type=str)
@click.option('--struct', required=False, type=str)
@click.option('--simulatortofmu', required=False, type=str)
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
