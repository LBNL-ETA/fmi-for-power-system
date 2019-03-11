from pymodelica import compile_fmu

fmu_name = compile_fmu("equation", "equation.mo",
                       version="2.0", target="me",
                       compiler_options={'extra_lib_dirs':["C:\\Users\\cyder\\Desktop\\SimulatorToFMU\\simulatortofmu\\parser\\libraries\\modelica"]})