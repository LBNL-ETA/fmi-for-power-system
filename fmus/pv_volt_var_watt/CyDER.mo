within ;
package CyDER
  package HIL

  end HIL;

  package Optimization
    package Examples
      model Test_voltage
      protected
        parameter Modelica.SIunits.Impedance Z11_601[2] = {0.3465, 1.0179};
        parameter Modelica.SIunits.Impedance Z12_601[2] = {0.1560, 0.5017};
        parameter Modelica.SIunits.Impedance Z13_601[2] = {0.1580, 0.4236};
        parameter Modelica.SIunits.Impedance Z22_601[2] = {0.3375, 1.0478};
        parameter Modelica.SIunits.Impedance Z23_601[2] = {0.1535, 0.3849};
        parameter Modelica.SIunits.Impedance Z33_601[2] = {0.3414, 1.0348};
      public
        parameter Real capctrl=1;
        Modelica.Blocks.Sources.Ramp ramp_incuctor(
          duration=1,
          startTime=1,
          offset=0.99,
          height=-0.98)
          annotation (Placement(transformation(extent={{100,20},{80,40}})));
        Buildings.Electrical.AC.ThreePhasesUnbalanced.Sources.FixedVoltage source1(
                                                                                  f=60, V=4.16e3)
                   annotation (Placement(transformation(extent={{-100,-10},{-80,10}})));
        Buildings.Electrical.AC.ThreePhasesUnbalanced.Loads.Inductive inductor(
          loadConn=Buildings.Electrical.Types.LoadConnection.wye_to_wyeg,
          mode=Buildings.Electrical.Types.Load.FixedZ_steady_state,
          V_nominal=4.16e3,
          use_pf_in=true,
          pf=0.005,
          P_nominal=-1000)
          annotation (Placement(transformation(extent={{40,30},{60,50}})));
        Chargepoint.Simulation.Components.Probe
                         sens_inductor
          annotation (Placement(transformation(extent={{0,30},{20,50}})));
        Chargepoint.Simulation.Components.Probe
                         sens_head
          annotation (Placement(transformation(extent={{-40,-10},{-20,10}})));
        Buildings.Electrical.AC.ThreePhasesUnbalanced.Lines.TwoPortMatrixRL line_650(
          Z11=2000/5280*Z11_601,
          Z12=2000/5280*Z12_601,
          Z13=2000/5280*Z13_601,
          Z22=2000/5280*Z22_601,
          Z23=2000/5280*Z23_601,
          Z33=2000/5280*Z33_601,
          V_nominal=4.16e3) annotation (Placement(transformation(
              extent={{-10,-10},{10,10}},
              rotation=0,
              origin={-50,0})));
        Chargepoint.Simulation.Components.Probe
                         sens_test
          annotation (Placement(transformation(extent={{-80,-10},{-60,10}})));
        Buildings.Electrical.AC.ThreePhasesUnbalanced.Loads.Capacitive capacitor(
          loadConn=Buildings.Electrical.Types.LoadConnection.wye_to_wyeg,
          mode=Buildings.Electrical.Types.Load.FixedZ_steady_state,
          V_nominal=1.16e3,
          use_pf_in=true,
          P_nominal=-1000,
          pf=0.005)
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Chargepoint.Simulation.Components.Probe
                         sens_capacitor
          annotation (Placement(transformation(extent={{0,-10},{20,10}})));
        Modelica.Blocks.Math.Gain gain(k=capctrl)
          annotation (Placement(transformation(extent={{0,-50},{20,-30}})));
        Modelica.Blocks.Sources.Constant const(k=1)
          annotation (Placement(transformation(extent={{-60,-50},{-40,-30}})));
        Modelica.Blocks.Interfaces.RealInput u
          annotation (Placement(transformation(extent={{30,-64},{70,-24}})));
      equation
        connect(sens_inductor.terminal_n,sens_head. terminal_p) annotation (Line(
              points={{0,40},{-10,40},{-10,0},{-20,0}}, color={0,120,120}));
        connect(sens_inductor.terminal_p,inductor. terminal)
          annotation (Line(points={{20,40},{40,40}}, color={0,120,120}));
        connect(ramp_incuctor.y,inductor. pf_in_3)
          annotation (Line(points={{79,30},{56.2,30}}, color={0,0,127}));
        connect(ramp_incuctor.y,inductor. pf_in_2)
          annotation (Line(points={{79,30},{64.5,30},{50,30}}, color={0,0,127}));
        connect(ramp_incuctor.y,inductor. pf_in_1)
          annotation (Line(points={{79,30},{44,30}}, color={0,0,127}));
        connect(sens_head.terminal_n,line_650. terminal_p)
          annotation (Line(points={{-40,0},{-40,0}}, color={0,120,120}));
        connect(source1.terminal,sens_test. terminal_n)
          annotation (Line(points={{-80,0},{-80,0}}, color={0,120,120}));
        connect(sens_test.terminal_p,line_650. terminal_n)
          annotation (Line(points={{-60,0},{-60,0}}, color={0,120,120}));
        connect(sens_capacitor.terminal_p,capacitor. terminal)
          annotation (Line(points={{20,0},{30,0},{40,0}}, color={0,120,120}));
        connect(sens_capacitor.terminal_n, sens_head.terminal_p)
          annotation (Line(points={{0,0},{-20,0}}, color={0,120,120}));
        connect(capacitor.pf_in_2, capacitor.pf_in_1) annotation (Line(points={{50,-10},
                {48,-10},{44,-10}},          color={0,0,127}));
        connect(capacitor.pf_in_3, capacitor.pf_in_2)
          annotation (Line(points={{56,-10},{50,-10}},          color={0,0,127}));
        connect(const.y, gain.u)
          annotation (Line(points={{-39,-40},{-20,-40},{-2,-40}}, color={0,0,127}));
        connect(capacitor.pf_in_2, u) annotation (Line(points={{50,-10},{54,-10},
                {54,-44},{50,-44}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Test_voltage;

      model Test_simple
        parameter Real capctrl=1;
        Modelica.Blocks.Math.Gain gain(k=capctrl)
          annotation (Placement(transformation(extent={{-20,40},{0,60}})));
        Modelica.Blocks.Interfaces.RealInput u
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
        Modelica.Blocks.Interfaces.RealOutput y
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
        Modelica.Blocks.Math.Add add
          annotation (Placement(transformation(extent={{20,-10},{40,10}})));
        Modelica.Blocks.Sources.Sine sine(amplitude=1, freqHz=2)
          annotation (Placement(transformation(extent={{-60,40},{-40,60}})));
      equation
        connect(add.y, y)
          annotation (Line(points={{41,0},{110,0},{110,0}}, color={0,0,127}));
        connect(add.u1, gain.y)
          annotation (Line(points={{18,6},{10,6},{10,50},{1,50}}, color={0,0,127}));
        connect(add.u2, u) annotation (Line(points={{18,-6},{-44,-6},{-44,0},{-120,0}},
              color={0,0,127}));
        connect(sine.y, gain.u) annotation (Line(points={{-39,50},{-30,50},{-22,
                50}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Test_simple;
    end Examples;
  end Optimization;

  package Development
    model voltWatt_param

      Modelica.Blocks.Interfaces.RealInput v(unit="1") "Voltage [p.u]"
        annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
      Modelica.Blocks.Interfaces.RealOutput PCon(unit="var")
        "P control signal"
        annotation (Placement(transformation(extent={{100,-10},{120,10}})));
      parameter Real thr(start=0.035) "over/undervoltage threshold";
      parameter Real hys(start=0.05) "Hysteresis";
      final parameter Modelica.SIunits.PerUnit vMaxDea=1 + hys "Upper bound of deaband [p.u.]";
      final parameter Modelica.SIunits.PerUnit vMax=1 + thr "Voltage maximum [p.u.]";
      parameter Real PMax(start=0, unit="W") "Maximal Active Power";
      parameter Real PMin(start=0, unit="W") "Minimal Reactive Power";
    equation
      PCon = smooth(0, if v > vMaxDea then PMin elseif v > vMax then (vMaxDea - v)/
        abs(vMax - vMaxDea)*PMax else PMax);
      annotation (Documentation(info="<html>
This model is similar to <a href=\"modelica://CyDER.HIL.Controls.voltVar\">
CyDER.HIL.Controls.voltVar</a> 
with the only differences that input variables have been 
changed to parameters.
</html>"));
    end voltWatt_param;

    model VoltVarWatt_param

      Modelica.Blocks.Interfaces.RealInput v(unit="1") "Voltage [p.u]"
        annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
      Modelica.Blocks.Interfaces.RealOutput PCon(unit="W")
        "Active power control signal"
        annotation (Placement(transformation(extent={{100,40},{120,60}})));
      parameter Real thr_p(start=0.035) "over/undervoltage threshold";
      parameter Real hys_p(start=0.05) "Hysteresis";
      final parameter Modelica.SIunits.PerUnit vMaxDea_p=1 + hys_p "Upper bound of deaband [p.u.]";
      final parameter Modelica.SIunits.PerUnit vMax_p=1 + thr_p "Voltage maximum [p.u.]";
      parameter Real PMax(start=0, unit="W") "Maximal Active Power";
      parameter Real PMin(start=0, unit="W") "Minimal Reactive Power";

      parameter Real thr_q(start=0.05) "over/undervoltage threshold";
      parameter Real hys_q(start=0.01) "Hysteresis";
      final parameter Modelica.SIunits.PerUnit vMaxDeaq=1 + hys_q "Upper bound of deaband [p.u.]";
      final parameter Modelica.SIunits.PerUnit vMaxq=1 + thr_q "Voltage maximum [p.u.]";
      final parameter Modelica.SIunits.PerUnit vMinDeaq=1 - hys_q "Upper bound of deaband [p.u.]";
      final parameter Modelica.SIunits.PerUnit vMinq=1 - thr_q "Voltage minimum [p.u.]";
      parameter Real QMaxInd(start=0, unit="var") "Maximal Reactive Power (Inductive)";
      parameter Real QMaxCap(start=0, unit="var") "Maximal Reactive Power (Capacitive)";
      Modelica.Blocks.Interfaces.RealOutput QCon(unit="var")
        "Reactive power control signal"
        annotation (Placement(transformation(extent={{100,-60},{120,-40}})));
    equation
      PCon = smooth(0, if v > vMaxDea_p then PMin elseif v > vMax_p then (vMaxDea_p - v)/
        abs(vMax_p - vMaxDea_p)*PMax else PMax);
      QCon = smooth(0, if v > vMax_q then QMaxInd*(-1) elseif v > vMaxDea_q then (vMaxDea_q - v)/
        abs(vMax_q - vMaxDea_q)*QMaxInd elseif v < vMin_q then QMaxCap elseif v < vMinDea_q then (
        vMinDea_q - v)/abs(vMin_q - vMinDea_q)*QMaxCap else 0);
      annotation (Documentation(info="<html>
This model is similar to <a href=\"modelica://CyDER.HIL.Controls.voltVar\">
CyDER.HIL.Controls.voltVar</a> 
with the only differences that input variables have been 
changed to parameters.
</html>"));
    end VoltVarWatt_param;

    model voltWatt_param_firstorder

      Modelica.Blocks.Interfaces.RealInput v(unit="1") "Voltage [p.u]"
        annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
      Modelica.Blocks.Interfaces.RealOutput QCon(unit="var") "Q control signal"
        annotation (Placement(transformation(extent={{100,-10},{120,10}})));
      parameter Real thr(start=0.05) "over/undervoltage threshold";
      parameter Real hys(start=0.01) "Hysteresis";
      final parameter Modelica.SIunits.PerUnit vMaxDea=1 + hys "Upper bound of deaband [p.u.]";
      final parameter Modelica.SIunits.PerUnit vMax=1 + thr "Voltage maximum [p.u.]";
      final parameter Modelica.SIunits.PerUnit vMinDea=1 - hys "Upper bound of deaband [p.u.]";
      final parameter Modelica.SIunits.PerUnit vMin=1 - thr "Voltage minimum [p.u.]";
      parameter Real PMax(start=0, unit="W") "Maximal Active Power";
      parameter Real PMin(start=0, unit="W") "Minimal Reactive Power";
      parameter Real Tfirstorder(unit="s") = 1 "Time constant of first order";
      Modelica.Blocks.Continuous.FirstOrder firstOrder(T=Tfirstorder)
        annotation (Placement(transformation(extent={{60,-10},{80,10}})));
      Development.voltWatt_param voltWatt_param1(
        thr=thr,
        hys=hys,
        PMax=PMax,
        PMin=PMin)
        annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
    equation

      connect(firstOrder.y, QCon)
        annotation (Line(points={{81,0},{94,0},{110,0}},        color={0,0,127}));
      connect(v, voltWatt_param1.v)
        annotation (Line(points={{-120,0},{-12,0}}, color={0,0,127}));
      connect(voltWatt_param1.PCon, firstOrder.u)
        annotation (Line(points={{11,0},{58,0}}, color={0,0,127}));
      annotation (Documentation(info="<html>
This model is similar to <a href=\"modelica://CyDER.HIL.Controls.voltVar\">
CyDER.HIL.Controls.voltVar</a> 
with the only differences that input variables have been 
changed to parameters.
</html>"));
    end voltWatt_param_firstorder;

    model Validate_VoltWattControl_param

      Modelica.Blocks.Sources.Ramp ramp(
        duration=1,
        startTime=0,
        height=0.2,
        offset=0.9)
        annotation (Placement(transformation(extent={{-90,-10},{-70,10}})));
      Development.voltWatt_param voltWat_param
        annotation (Placement(transformation(extent={{-36,-10},{-16,10}})));
    equation
      connect(voltWat_param.v, ramp.y)
        annotation (Line(points={{-38,0},{-69,0}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
            coordinateSystem(preserveAspectRatio=false)));
    end Validate_VoltWattControl_param;

    model Validate_VoltVarWattControl_param

      Modelica.Blocks.Sources.Ramp ramp(
        duration=1,
        startTime=0,
        height=0.2,
        offset=0.9)
        annotation (Placement(transformation(extent={{-90,-10},{-70,10}})));
      Development.VoltVarWatt_param voltVarWat_param
        annotation (Placement(transformation(extent={{-44,-10},{-24,10}})));
    equation
      connect(ramp.y, voltVarWat_param.v)
        annotation (Line(points={{-69,0},{-46,0}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
            coordinateSystem(preserveAspectRatio=false)));
    end Validate_VoltVarWattControl_param;
  end Development;

  package Controls

    package Model
      model voltVar

        Modelica.Blocks.Interfaces.RealInput v_pu "Voltage [p.u.]"
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
        Modelica.Blocks.Interfaces.RealOutput q_control "Q control signal"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
        Modelica.Blocks.Interfaces.RealInput v_maxdead
          "Upper bound of deadband [p.u.]"
          annotation (Placement(transformation(extent={{-140,20},{-100,60}})));
        Modelica.Blocks.Interfaces.RealInput v_max "Voltage maximum [p.u.]"
          annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
        Modelica.Blocks.Interfaces.RealInput v_mindead
          "Upper bound of deadband [p.u.]"
          annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
        Modelica.Blocks.Interfaces.RealInput v_min "Voltage minimum [p.u.]"
          annotation (Placement(transformation(extent={{-140,-100},{-100,-60}})));
        Modelica.Blocks.Interfaces.RealInput q_maxind "Maximal Reactive Power (Inductive)" annotation (
            Placement(transformation(
              extent={{-20,-20},{20,20}},
              rotation=270,
              origin={20,120})));
        Modelica.Blocks.Interfaces.RealInput q_maxcap "Maximal Reactive Power (Capacitive)" annotation (
            Placement(transformation(
              extent={{-20,-20},{20,20}},
              rotation=270,
              origin={-40,120})));
      equation
        q_control = smooth(0,
          if v_pu > v_max then q_maxind * (-1)
          elseif v_pu > v_maxdead then (v_maxdead - v_pu)/abs(v_max - v_maxdead) * q_maxind
          elseif v_pu < v_min then q_maxcap
          elseif v_pu < v_mindead then (v_mindead - v_pu)/abs(v_min - v_mindead) * q_maxcap
          else 0);
      end voltVar;

      model voltVar_param

        Modelica.Blocks.Interfaces.RealInput v(start = 1, unit="1") "Voltage [p.u]"
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
        Modelica.Blocks.Interfaces.RealOutput QCon(start= 0, unit="var") "Q control signal"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
        parameter Real thr = 0.05 "over/undervoltage threshold";
        parameter Real hys = 0.01 "Hysteresis";
        final parameter Modelica.SIunits.PerUnit vMaxDea=1 + hys "Upper bound of deaband [p.u.]";
        final parameter Modelica.SIunits.PerUnit vMax=1 + thr "Voltage maximum [p.u.]";
        final parameter Modelica.SIunits.PerUnit vMinDea=1 - hys "Upper bound of deaband [p.u.]";
        final parameter Modelica.SIunits.PerUnit vMin=1 - thr "Voltage minimum [p.u.]";
        parameter Real QMaxInd(unit="var") = 1000 "Maximal Reactive Power (Inductive)";
        parameter Real QMaxCap(unit="var") = 1000 "Maximal Reactive Power (Capacitive)";
      equation
        QCon = smooth(0, if v > vMax then QMaxInd*(-1) elseif v > vMaxDea then (vMaxDea - v)/
          abs(vMax - vMaxDea)*QMaxInd elseif v < vMin then QMaxCap elseif v < vMinDea then (
          vMinDea - v)/abs(vMin - vMinDea)*QMaxCap else 0);
        annotation (Documentation(info="<html>
This model is similar to <a href=\"modelica://CyDER.HIL.Controls.voltVar\">
CyDER.HIL.Controls.voltVar</a> 
with the only differences that input variables have been 
changed to parameters.
</html>"));
      end voltVar_param;

      model voltVar_param_firstorder

        Modelica.Blocks.Interfaces.RealInput v(start=1, unit="1") "Voltage [p.u]"
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
        Modelica.Blocks.Interfaces.RealOutput QCon(start=0, unit="var") "Q control signal"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
        parameter Real thr = 0.05 "over/undervoltage threshold";
        parameter Real hys= 0.01 "Hysteresis";
        final parameter Modelica.SIunits.PerUnit vMaxDea=1 + hys "Upper bound of deaband [p.u.]";
        final parameter Modelica.SIunits.PerUnit vMax=1 + thr "Voltage maximum [p.u.]";
        final parameter Modelica.SIunits.PerUnit vMinDea=1 - hys "Upper bound of deaband [p.u.]";
        final parameter Modelica.SIunits.PerUnit vMin=1 - thr "Voltage minimum [p.u.]";
        parameter Real QMaxInd(unit="var") = 1000 "Maximal Reactive Power (Inductive)";
        parameter Real QMaxCap(unit="var") = 1000 "Maximal Reactive Power (Capacitive)";
        parameter Real Tfirstorder(unit="s") = 1 "Time constant of first order";
        Model.voltVar_param voltVar_param1(
          thr=thr,
          hys=hys,
          QMaxInd=QMaxInd,
          QMaxCap=QMaxCap)
          annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
        Modelica.Blocks.Continuous.FirstOrder firstOrder(T=Tfirstorder)
          annotation (Placement(transformation(extent={{60,-10},{80,10}})));
      equation

        connect(voltVar_param1.v, v)
          annotation (Line(points={{-12,0},{-120,0}}, color={0,0,127}));
        connect(voltVar_param1.QCon, firstOrder.u)
          annotation (Line(points={{11,0},{11,0},{58,0}}, color={0,0,127}));
        connect(firstOrder.y, QCon)
          annotation (Line(points={{81,0},{94,0},{110,0}},        color={0,0,127}));
        annotation (Documentation(info="<html>
This model is similar to <a href=\"modelica://CyDER.HIL.Controls.voltVar\">
CyDER.HIL.Controls.voltVar</a> 
with the only differences that input variables have been 
changed to parameters.
</html>"));
      end voltVar_param_firstorder;

      model voltVarWatt_param_firstorder

        Modelica.Blocks.Interfaces.RealInput v(start=1, unit="1") "Voltage [p.u]"
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
        Modelica.Blocks.Interfaces.RealOutput Qctrl(start=0, unit="var")
          "Reactive power control signal"
          annotation (Placement(transformation(extent={{100,-60},{120,-40}})));

        parameter Real thrP = 0.05 "P: over/undervoltage threshold";
        parameter Real hysP= 0.04 "P: Hysteresis";

        parameter Real thrQ = 0.04 "Q: over/undervoltage threshold";
        parameter Real hysQ = 0.01 "Q: Hysteresis";
        parameter Real QMaxInd(unit="var") = 1000 "Maximal Reactive Power (Inductive)";
        parameter Real QMaxCap(unit="var") = 1000 "Maximal Reactive Power (Capacitive)";

        parameter Real Tfirstorder(unit="s") = 1 "Time constant of first order";

        Model.voltVar_param_firstorder voltWatt(
          Tfirstorder=Tfirstorder,
          thr=thrP,
          hys=hysP,
          QMaxInd=-1,
          QMaxCap=0)
          annotation (Placement(transformation(extent={{-8,40},{12,60}})));
        Model.voltVar_param_firstorder voltVar(
          thr=thrQ,
          hys=hysQ,
          QMaxInd=QMaxInd,
          QMaxCap=QMaxCap,
          Tfirstorder=Tfirstorder)
          annotation (Placement(transformation(extent={{-8,-60},{12,-40}})));
        Modelica.Blocks.Interfaces.RealOutput Plim(start=1, unit="1")
          "Reactive power control signal"
          annotation (Placement(transformation(extent={{100,40},{120,60}})));
        Modelica.Blocks.Math.Add sub(k2=-1)
          annotation (Placement(transformation(extent={{40,40},{60,60}})));
        Modelica.Blocks.Sources.Constant const_p(k=1)
          annotation (Placement(transformation(extent={{0,70},{20,90}})));
      equation

        connect(voltVar.QCon, Qctrl)
          annotation (Line(points={{13,-50},{110,-50}}, color={0,0,127}));
        connect(voltWatt.v, v) annotation (Line(points={{-10,50},{-40,50},{-40,0},{-120,
                0}}, color={0,0,127}));
        connect(voltVar.v, v) annotation (Line(points={{-10,-50},{-40,-50},{-40,0},{-120,
                0}}, color={0,0,127}));
        connect(sub.y, Plim)
          annotation (Line(points={{61,50},{110,50}}, color={0,0,127}));
        connect(sub.u2, voltWatt.QCon) annotation (Line(points={{38,44},{20,44},{20,50},
                {13,50}}, color={0,0,127}));
        connect(const_p.y, sub.u1) annotation (Line(points={{21,80},{30,80},{30,56},{38,
                56}}, color={0,0,127}));
        annotation (Documentation(info="<html>
This model is similar to <a href=\"modelica://CyDER.HIL.Controls.voltVar\">
CyDER.HIL.Controls.voltVar</a> 
with the only differences that input variables have been 
changed to parameters.
</html>"));
      end voltVarWatt_param_firstorder;
    end Model;

    package Examples
      model Validate_VoltVarControl

        Modelica.Blocks.Sources.Ramp ramp(
          duration=1,
          startTime=0,
          height=0.2,
          offset=0.9)
          annotation (Placement(transformation(extent={{-90,-10},{-70,10}})));
        Modelica.Blocks.Sources.Constant upper_voltage(k=1.05)
          annotation (Placement(transformation(extent={{-60,50},{-40,70}})));
        Modelica.Blocks.Sources.Constant lower_voltage(k=0.95)
          annotation (Placement(transformation(extent={{-60,-70},{-40,-50}})));
        Model.voltVar voltVar
          annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
        Modelica.Blocks.Sources.Constant upper_deadband_voltage(k=1.01)
          annotation (Placement(transformation(extent={{-60,10},{-40,30}})));
        Modelica.Blocks.Sources.Constant lower_deadband_voltage(k=0.99)
          annotation (Placement(transformation(extent={{-60,-30},{-40,-10}})));
        Modelica.Blocks.Sources.Constant qmax_inductive(k=1) annotation (Placement(
              transformation(
              extent={{-10,-10},{10,10}},
              rotation=-90,
              origin={40,60})));
        Modelica.Blocks.Sources.Constant qmax_capacitive(k=0.2) annotation (Placement(
              transformation(
              extent={{-10,-10},{10,10}},
              rotation=-90,
              origin={0,60})));
      equation
        connect(ramp.y, voltVar.v_pu)
          annotation (Line(points={{-69,0},{-12,0}}, color={0,0,127}));
        connect(lower_voltage.y, voltVar.v_min) annotation (Line(points={{-39,
                -60},{-20,-60},{-20,-8},{-12,-8}}, color={0,0,127}));
        connect(upper_voltage.y, voltVar.v_max) annotation (Line(points={{-39,
                60},{-20,60},{-20,8},{-12,8}}, color={0,0,127}));
        connect(voltVar.v_mindead, lower_deadband_voltage.y) annotation (Line(
              points={{-12,-4},{-30,-4},{-30,-20},{-39,-20}}, color={0,0,127}));
        connect(upper_deadband_voltage.y, voltVar.v_maxdead) annotation (Line(
              points={{-39,20},{-30,20},{-30,4},{-12,4}}, color={0,0,127}));
        connect(qmax_capacitive.y, voltVar.q_maxcap) annotation (Line(points={{-1.9984e-015,
                49},{0,49},{0,30},{-4,30},{-4,12}}, color={0,0,127}));
        connect(qmax_inductive.y, voltVar.q_maxind) annotation (Line(points={{40,49},{40,
                49},{40,40},{12,40},{12,20},{2,20},{2,12}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Validate_VoltVarControl;

      model Validate_VoltVarControl_param

        Modelica.Blocks.Sources.Ramp ramp(
          duration=1,
          startTime=0,
          height=0.2,
          offset=0.9)
          annotation (Placement(transformation(extent={{-90,-10},{-70,10}})));
        Model.voltVar_param voltVar_param
          annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
      equation
        connect(voltVar_param.v, ramp.y)
          annotation (Line(points={{-12,0},{-69,0}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Validate_VoltVarControl_param;

      model Validate_VoltVarWattControl
        Modelica.Blocks.Sources.Ramp ramp(
          duration=1,
          startTime=0,
          height=0.2,
          offset=0.9)
          annotation (Placement(transformation(extent={{-90,-10},{-70,10}})));
        Model.voltVarWatt_param_firstorder voltVarWatt_param_firstorder(
            Tfirstorder=0.001)
          annotation (Placement(transformation(extent={{-8,-10},{12,10}})));
      equation
        connect(voltVarWatt_param_firstorder.v, ramp.y)
          annotation (Line(points={{-10,0},{-69,0}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Validate_VoltVarWattControl;
    end Examples;
  end Controls;

  package uPMU
    model uPMU_API
      Buildings.Utilities.IO.Python27.Real_Real Placeholder
        annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
            coordinateSystem(preserveAspectRatio=false)));
    end uPMU_API;
  end uPMU;

  package Simulation
    package Model
      model Pv_Inv_VoltVarWatt_simple
        // Weather data
        parameter String weather_file "Path to weather file";
        // PV generation
        parameter Real n(min=0, unit="1") = 14 "Number of PV modules";
        parameter Modelica.SIunits.Area A(min=0) = 1.65 "Net surface area per module [m2]";
        parameter Real eta(min=0, max=1, unit="1") = 0.158
          "Module conversion efficiency";
        parameter Real lat(unit="deg") = 37.9 "Latitude [deg]";
        parameter Real til(unit="deg") = 10 "Surface tilt [deg]";
        parameter Real azi(unit="deg") = 0 "Surface azimuth [deg] 0-S, 90-W, 180-N, 270-E ";
        // VoltVarWatt
        parameter Real thrP = 0.05 "P: over/undervoltage threshold";
        parameter Real hysP= 0.04 "P: Hysteresis";
        parameter Real thrQ = 0.04 "Q: over/undervoltage threshold";
        parameter Real hysQ = 0.01 "Q: Hysteresis";
        parameter Real QMaxInd(unit="var") = 1000 "Maximal Reactive Power (Inductive)";
        parameter Real QMaxCap(unit="var") = 1000 "Maximal Reactive Power (Capacitive)";
        parameter Real Tfirstorder(unit="s") = 1 "Time constant of first order";

        SmartInverter.Components.Photovoltaics.PVModule_simple pVModule_simple(
          n=n,
          A=A,
          eta=eta,
          lat=lat,
          til=til,
          azi=azi)
          annotation (Placement(transformation(extent={{-10,40},{10,60}})));
        Buildings.BoundaryConditions.WeatherData.ReaderTMY3 weaDatInpCon(
            computeWetBulbTemperature=false, filNam=weather_file)
          "Weather data reader with radiation data obtained from the inputs' connectors"
          annotation (Placement(transformation(extent={{-80,60},{-60,80}})));
        Controls.Model.voltVarWatt_param_firstorder voltVarWatt_param_firstorder
          annotation (Placement(transformation(extent={{-50,-10},{-30,10}})));
        Modelica.Blocks.Interfaces.RealInput v(start=1, unit="1") "Voltage [p.u]"
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
        Modelica.Blocks.Interfaces.RealOutput Q(start=0, unit="var") "Reactive power"
          annotation (Placement(transformation(extent={{100,-60},{120,-40}})));
        Modelica.Blocks.Interfaces.RealOutput P(start=1, unit="1") "Active power"
          annotation (Placement(transformation(extent={{100,40},{120,60}})));
      equation
        connect(weaDatInpCon.weaBus, pVModule_simple.weaBus) annotation (Line(
            points={{-60,70},{-40,70},{-40,54},{-10,54}},
            color={255,204,51},
            thickness=0.5));
        connect(voltVarWatt_param_firstorder.v, v)
          annotation (Line(points={{-52,0},{-120,0}}, color={0,0,127}));
        connect(pVModule_simple.scale, voltVarWatt_param_firstorder.Plim) annotation (
           Line(points={{-12,46},{-20,46},{-20,5},{-29,5}}, color={0,0,127}));
        connect(voltVarWatt_param_firstorder.Qctrl, Q) annotation (Line(points={{-29,-5},
                {-20,-5},{-20,-50},{110,-50}}, color={0,0,127}));
        connect(pVModule_simple.P, P)
          annotation (Line(points={{11,50},{110,50}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Pv_Inv_VoltVarWatt_simple;
    end Model;

    package Examples
    end Examples;
  end Simulation;
  annotation (uses(Modelica(version="3.2.2"), Buildings(version="4.0.0"),
      SmartInverter(version="5")));
end CyDER;
