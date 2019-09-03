from pymodelica import compile_fmu

fmu_name = compile_fmu("pandapower", "pandapower.mo",compiler_log_level="d",
                       version="2.0", target="me",
                       compiler_options={'extra_lib_dirs':["C:\\Users\\DRRC\\Desktop\\Joscha\\SimulatorToFMU\\simulatortofmu\\parser\\libraries\\modelica"]})