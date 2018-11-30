from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='cydertool',
    description='Functions to compile and launch simulations for PyFMI',
    author='Jonathan Coignard',
    author_email='JCoignard@lbl.gov',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points='''
        [console_scripts]
        cyderc=cydertool.utility:compile_cmd
        cyders=cydertool.utility:simulate_cmd
    ''',
)
