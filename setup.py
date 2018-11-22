from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='cydertool',
    description='',
    author='',
    author_email='',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required
    entry_points='''
        [console_scripts]
        utility=cydertool.scripts.utility:cli
    ''',
)


config = {
    'description': 'Clustering event on the grid',
    'author': 'Armando Domingos, Jonathan Coignard',
    'author_email': 'armando.domingos@berkeley.edu, jcoignard@lbl.gov',
    'version': '0.0.1',
    'install_requires': required,
    'packages': ['gridevent', 'gridevent.utility'],
    'name': 'gridevent',
    'include_package_data': False,
}

setup(**config)
