# coding: utf-8
import click
import json
import pandas
from pyfmi import load_fmu
from pyfmi.fmi_coupled import CoupledFMUModelME2


# Load FMUs, connect them and launch the simulation
@click.command()
@click.option('--start', required=True, type=int)
@click.option('--end', required=True, type=int)
@click.option('--connections', required=True, type=str)
@click.option('--fmutype', required=False, type=str)
@click.option('--steps', required=False, type=int)
def simulate(start, end, connections, fmu_type='me', nb_steps=500):
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
