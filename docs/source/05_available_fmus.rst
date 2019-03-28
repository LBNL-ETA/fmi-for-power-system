Available FMUs
==============

CYME FMU
--------
The CYME FMU can be downloaded from `here <https://github.com/LBNL-ETA/fmi-for-power-system/tree/master/tests/005_multiplier_with_cyme/cyme>`_.

An example of model description is provided below. A few things are required for the CYME FMU to operate properly:
  - a parameter called _configurationFileName pointing to a JSON configuration file (including the feeder filename).
  - inputs and outputs should have the following format {NETWORK ID}!{NODE/LOAD ID}!{KEYWORD}, where KEYWORD can be KW, KVAR, or Vpu.

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8"?>
  <SimulatorModelDescription
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  fmiVersion="2.0"
  modelName="simulator"
  description="Input data for a Simulator FMU"
  generationTool="SimulatorToFMU">
  <ModelVariables>
    <ScalarVariable
      name="_configurationFileName"
      description="parameter"
      causality="parameter"
      start="C:\\Users\\DRRC\\Desktop\\fmi-for-power-system\\tests\\005_multiplier_with_cyme\\cyme\\jonathan.json2"
      type="String">
    </ScalarVariable>
    <ScalarVariable
      name="IEEE34NODES!836!KW"
      description="input P"
      causality="input"
      type="Real"
      unit="kW">
    </ScalarVariable>
    <ScalarVariable
      name="IEEE34NODES!836!KVAR"
      description="input Q"
      causality="input"
      type="Real"
      unit="kW">
    </ScalarVariable>
    <ScalarVariable
      name="voltage!836!Vpu"
      description="output voltage p.u."
      causality="output"
      type="Real">
    </ScalarVariable>
  </ModelVariables>
  </SimulatorModelDescription>

The JSON configuration file should have the following format:

.. code-block:: json

  {
    "model_filename": "IEEE_34_node_test_feeder.sxst",
    "total_load_filename":"total_load.csv",
    "substation_network":"IEEE34NODES"
  }

PandaPower FMU
--------------
The PandaPower FMU can be downloaded `here <https://github.com/LBNL-ETA/fmi-for-power-system/tree/master/tests/014_pandapower_test_default/pandapower>`_.

An example of model description is provided below. Note that this FMU does not require any configuration file since the feeder model is set within the FMU.

.. code-block:: xml

  <?xml version='1.0' encoding='UTF-8'?>
  <SimulatorModelDescription
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    fmiVersion="2.0"
    modelName="pandapower"
    description="pandapower" generationTool="SimulatorToFMU">
    <ModelVariables>
      <ScalarVariable name="KW_7"
        description="_" causality="input" type="Real" unit="_"/>
      <ScalarVariable name="KVAR_7"
        description="_" causality="input" type="Real" unit="_"/>
      <ScalarVariable name="Vpu_7"
        description="_" causality="output" type="Real" unit="_"/>
      <ScalarVariable name="Vpu_12"
        description="_" causality="output" type="Real" unit="_"/>
    </ModelVariables>
  </SimulatorModelDescription>


Template Python FMU
-------------------
A simple template for creating Python FMU can be found `here <https://github.com/LBNL-ETA/fmi-for-power-system/tree/master/fmus/simple_func>`_.

Note: If the name of the FMU is set to "NAME" in the XML file then the Python file with the "exchange" function should be named "NAME_wrapper.py"

Note: The FMU needs to be recompiled anytime it is moved to a different folder or any inputs/outputs names are changed.


Template Server FMU
-------------------
A simple template for creating Server FMU can be found `here <https://github.com/LBNL-ETA/fmi-for-power-system/tree/master/tests/007_server_algebraic_loop/bbq>`_.
