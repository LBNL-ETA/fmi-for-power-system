from pymodelica import compile_fmu

fmu_name = compile_fmu("pandapower", "pandapower.mo",
                       version="2.0", target="me",
                       compiler_options={'extra_lib_dirs':["C:\\Users\\DRRC\\Desktop\\desktops\\February\\SimulatorToFMU\\simulatortofmu\\parser\\libraries\\modelica"]})