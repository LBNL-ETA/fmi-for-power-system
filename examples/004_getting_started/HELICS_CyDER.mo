within ;
package HELICS_CyDER
  model Generator "Generate a sinewave"
    Real x "state variable";
    Modelica.Blocks.Interfaces.RealOutput y "output" annotation (Placement(transformation(
            extent={{100,-8},{120,12}}), iconTransformation(extent={{100,-8},{120,
              12}})));
  equation
    der(x) = sin(time);
    y = 5.5*x + 115;
  end Generator;

  model Controller
    "On/Off Controller"
    Modelica.Blocks.Interfaces.RealInput u "input" annotation (Placement(transformation(
            extent={{-140,-20},{-100,20}}), iconTransformation(extent={{-140,-20},
              {-100,20}})));
    Modelica.Blocks.Interfaces.RealOutput y "output" annotation (Placement(transformation(
            extent={{100,-8},{120,12}}), iconTransformation(extent={{100,-8},{120,
              12}})));
  equation
    if (u > 120.0) then
      y = 0.0;
    else
      y = 1.0;
    end if;
  end Controller;

  model Scaling "Scale the output"
    parameter Real fac=1/120 "scaling factor";
    Modelica.Blocks.Interfaces.RealInput u "input" annotation (Placement(transformation(
            extent={{-140,-20},{-100,20}}), iconTransformation(extent={{-140,-20},
              {-100,20}})));
    Modelica.Blocks.Interfaces.RealOutput y "output" annotation (Placement(transformation(
            extent={{100,-8},{120,12}}), iconTransformation(extent={{100,-8},{120,
              12}})));
  equation
    y = u*fac;
  end Scaling;

  model TestCoupledSystem

    Generator voltage
      annotation (Placement(transformation(extent={{-56,-10},{-36,10}})));
    Controller controller
      annotation (Placement(transformation(extent={{24,-10},{44,10}})));
  equation
    connect(voltage.y, controller.u) annotation (Line(points={{-35,0.2},{-5.5,
            0.2},{-5.5,0},{22,0}}, color={0,0,127}));
  end TestCoupledSystem;
  annotation (uses(Modelica(version="3.2.2")));
end HELICS_CyDER;
