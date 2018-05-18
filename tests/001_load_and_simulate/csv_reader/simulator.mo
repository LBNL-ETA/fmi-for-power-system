model simulator
  "Block that exchanges a vector of real values with Simulator"
  extends Modelica.Blocks.Interfaces.BlockIcon;

///////////// THE CODE BELOW HAS BEEN AUTOGENERATED //////////////
  Modelica.Blocks.Interfaces.RealInput column(start=0.0, unit="V")
    "input" annotation(Placement(transformation(extent={{-122,68},{-100,90}})));
  Modelica.Blocks.Interfaces.RealOutput y (unit="A")
    "output" annotation(Placement(transformation(extent={{100,70},{120,90}})));
  // Configuration specific parameters coming from 
  // the inputs of the Python export tool (SimulatorToFMU.py) 
  parameter String patResScri = Modelica.Utilities.Files.loadResource("C:\\Users\\DRRC\\Desktop\\fmi-for-power-system\\tests\\001_load_and_simulate\\csv_reader\\start_server.bat")
    "Path to the script in resource folder";
  // used to generate the FMU
  parameter String _configurationFileName = Modelica.Utilities.Files.loadResource("C:\\Users\\DRRC\\Desktop\\fmi-for-power-system\\tests\\001_load_and_simulate\\csv_reader\\data.csv")
    "Path to the configuration or input file";
  parameter Boolean _saveToFile (fixed=true) = false "Flag for writing results"; 
  
protected
   parameter String runServer = Modelica.Utilities.Files.loadResource("C:\\Users\\DRRC\\Desktop\\fmi-for-power-system\\tests\\001_load_and_simulate\\csv_reader\\run_server.py")
    "Path to the script to run the server";
  SimulatorToFMU.Server.Functions.BaseClasses.ServerObject obj=
  SimulatorToFMU.Server.Functions.BaseClasses.ServerObject(patResScri=patResScri,
    patConFil=_configurationFileName);
  
   parameter Integer nDblPar=0 
    "Number of double parameter values to sent to Simulator";
  parameter Integer nDblInp(min=1)=1 
    "Number of double input values to sent to Simulator";
  parameter Integer nDblOut(min=1)=1  
    "Number of double output values to receive from Simulator";
  
  Real dblInpVal[nDblInp] "Value to be sent to Simulator";
  
  
  Real uR[nDblInp]={
  column 
  }"Variables used to collect values to be sent to Simulator";
   
  Real yR[nDblOut]={
  y 
  }"Variables used to collect values received from Simulator";
  
  parameter String dblInpNam[nDblInp]={
  "column" 
  }"Input variable name to be sent to Simulator";
  
  parameter String dblOutNam[nDblOut]={
  "y" 
  }"Output variable names to be received from Simulator";
  parameter String dblParNam[nDblPar]
    "Parameter variable names to be sent to Simulator";
  parameter Real dblParVal[nDblPar]=zeros(nDblPar)
    "Parameter variable values to be sent to Simulator";
  
///////////// THE CODE ABOVE HAS BEEN AUTOGENERATED //////////////  
  protected

  equation 
	// Compute values that will be sent to Simulator
	for _cnt in 1:nDblInp loop
	  dblInpVal[_cnt] = uR[_cnt];
	end for;
	  
	// Exchange data
	yR = SimulatorToFMU.Server.Functions.simulator(
	  modTim=time,
	  nDblInp=nDblInp,
	  dblInpNam=dblInpNam,
	  dblInpVal=dblInpVal,
	  nDblOut=nDblOut,
	  dblOutNam=dblOutNam,
	  nDblPar=nDblPar,
	  dblParNam=dblParNam,
	  dblParVal=dblParVal,
	  resWri=_saveToFile,
	  obj=obj); 
end simulator;