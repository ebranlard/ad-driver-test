
# Test cases for aerodyn driver


Features:
 - regular analysis, time series analysis, combined cases analyses
 - with or wihtout inflowind
 - basic or advanced rotor inputs
 - OLAF or BEM
 - regular HAWT, or general multi-bladed rotors
 - multiple rotors
 - rotors with no blades and tower only
 - motions: sinusoidal motion of the base, general motion of the base, general motion for yaw, rotor speed and pitch


BEM test cases ("realistic"):

 - ad\_timeseries\_shutdown: NREL5MW rotor, time series analysis, without inflow wind  
 - MultipleHAWT: multiple BAR rotors, regular analysis type, mixed basic/advanced rotor inputs

BEM test cases (feature testing):

 - BAR\_CombinedCases:  BAR rotor, combined case analysis type
 - BAR\_SineMotion: BAR rotor, regular analysis type, sine motion of the base 
 - BAR\_RNAMotion: BAR rotor, regular analysis type, advanced rotor inputs, genereral motion of yaw/pitch and rotor speed, unrealistic case


OLAF test cases ("realistic"):

 - BAR\_OLAF : BAR rotor, regular analysis type, basic rotor inputs, no inflow wind, realistic setup


OLAF test cases ("analytical"):

 - EllipticalWingInf\_OLAF : one elliptical wing, regular analysis type,  advanced rotor inputs, inflowwind, no wake rollup in OLAF and large time step
 - HelicalWakeInf\_OLAF: "fake" three blades, regular analysis type, advanced rotor inputs, no wake rollup in OLAF


OLAF test cases (for feature testing):

 - VerticalAxis\_OLAF: three bladed H rotor, regular analysis type
 - Kite\_OLAF
 - QuadRotor\_OLAF



