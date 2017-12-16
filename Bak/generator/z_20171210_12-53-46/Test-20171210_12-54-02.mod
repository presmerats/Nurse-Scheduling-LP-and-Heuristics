 /*********************************************
 * OPL 12.6.0.0 Model
 * Author: Adrian Rodriguez Bazaga, Pau Rodriguez Esmerats
 * Creation Date: 06/12/2017 at 14:53:13
 *********************************************/

 
 main {


function cleanString(mystring){
	
	var returnstring = "";
	var i = mystring.indexOf("\n");
	var aux2 = mystring;
	var j=0;
	while (i != -1 && j<100){
		var aux = aux2.substring(0,i);
		aux2 = aux2.substring(i+1);
		returnstring = returnstring + aux + "\\n";
		i = aux2.indexOf("\n");
		j = j +1;
	}

	return returnstring;
}

function myTest(def, cplex, filename, logname, goal, objf, showsol) {

 var ofile = new IloOplOutputFile(logname, true);
 ofile.write("{ \""+filename+"\" : ");
 ofile.write("{");
 //ofile.writeln("\"\" : \""++"\",");
 
 var model = new IloOplModel(def,cplex);
 
 var data = new IloOplDataSource(filename);
 model.addDataSource(data);
 model.generate();
 //cplex.epgap=0.01;
 // 
 // 3600.0 1h
 // 1800.0 30m
 // 900.0 15m
 // 300.0 5m
 //  60.0 1m
 cplex.TiLim=300.0;
 //model.setParam(IloCplex.Param.tune.DetTimeLimit,10.0);
 
 //try {

  var solved = cplex.solve();  
  ofile.writeln("\"expected_output\" : \""+goal+"\",");
  ofile.writeln("\"computed_output\" : \""+solved+"\",");
  ofile.writeln("\"desired_objfunc\" : \""+objf+"\",");
	
	if (solved){
	 	
	 	ofile.writeln("\"time\" : \""+cplex.getSolvedTime()+"\",");
	 	ofile.writeln("\"int_vars\" : \""+cplex.getNintVars()+"\",");
	 	//ofile.writeln("\"lower_bound\" : \""+cplex.getLb()+"\",");
	 	ofile.writeln("\"Gap\" : \""+cplex.getMIPRelativeGap()+"\",");
	 	ofile.writeln("\"ObjectiveFunction\" : \""+cplex.getObjValue()+"\",");
	 	ofile.writeln("\"isMIP?\" : \""+cplex.isMIP()+"\",");
	 	ofile.writeln("\"Data\" : \""+cleanString(model.printExternalData())+"\",");
	 	ofile.writeln("\"Solution\" : \""+cleanString(model.printSolution())+"\"");
 	} else {
		ofile.writeln("\"Data\" : \""+cleanString(model.printExternalData())+"\"");
	
 	}	 	

 	
	  
// } catch (IloException e){
//  	ofile.writeln("                --- Exception Occurred for : "+filename )
//	ofile.writeln(model.printExternalData());	
//	ofile.writeln(e.printStackTrace());
// }

 ofile.write("}},");

 ofile.close();
 data.end();
 model.end();
  return true;
}




var src = new IloOplModelSource("model01-hfree.mod");

var def = new IloOplModelDefinition(src);

var cplex = new IloCplex();

var logname = "log-tests-model01-hfree-"+cplex.getCplexTime()+".txt"
var ofile = new IloOplOutputFile(logname, true);
ofile.writeln("[");
ofile.close();






myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-16mxH-12mnH-3Cnt-20171210_12-53-58912.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-16mxH-12mnH-3Cnt-20171210_12-53-58351.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-16mxH-12mnH-2Cnt-20171210_12-53-57763.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-16mxH-12mnH-2Cnt-20171210_12-53-57744.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-16mxH-12mnH-1Cnt-20171210_12-53-57787.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-16mxH-12mnH-1Cnt-20171210_12-53-57385.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-16mxH-1mnH-3Cnt-20171210_12-53-57361.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-16mxH-1mnH-3Cnt-20171210_12-53-57272.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-16mxH-1mnH-2Cnt-20171210_12-53-57349.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-16mxH-1mnH-2Cnt-20171210_12-53-56788.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-16mxH-1mnH-1Cnt-20171210_12-53-56935.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-16mxH-1mnH-1Cnt-20171210_12-53-56909.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-8mxH-6mnH-3Cnt-20171210_12-53-59505.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-8mxH-6mnH-3Cnt-20171210_12-53-59206.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-8mxH-6mnH-2Cnt-20171210_12-53-59607.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-8mxH-6mnH-2Cnt-20171210_12-53-59152.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-8mxH-6mnH-1Cnt-20171210_12-53-59963.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-8mxH-6mnH-1Cnt-20171210_12-53-59698.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-8mxH-1mnH-3Cnt-20171210_12-53-59941.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-8mxH-1mnH-3Cnt-20171210_12-53-58296.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-8mxH-1mnH-2Cnt-20171210_12-53-58838.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-8mxH-1mnH-2Cnt-20171210_12-53-58107.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-8mxH-1mnH-1Cnt-20171210_12-53-58585.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-16mxC-8mxH-1mnH-1Cnt-20171210_12-53-58356.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-16mxH-12mnH-3Cnt-20171210_12-54-01555.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-16mxH-12mnH-3Cnt-20171210_12-54-01255.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-16mxH-12mnH-2Cnt-20171210_12-54-01142.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-16mxH-12mnH-2Cnt-20171210_12-54-00448.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-16mxH-12mnH-1Cnt-20171210_12-54-00539.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-16mxH-12mnH-1Cnt-20171210_12-54-00209.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-16mxH-1mnH-3Cnt-20171210_12-54-00703.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-16mxH-1mnH-3Cnt-20171210_12-54-00166.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-16mxH-1mnH-2Cnt-20171210_12-54-00236.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-16mxH-1mnH-2Cnt-20171210_12-53-59639.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-16mxH-1mnH-1Cnt-20171210_12-53-59650.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-16mxH-1mnH-1Cnt-20171210_12-53-59284.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-8mxH-6mnH-3Cnt-20171210_12-54-02872.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-8mxH-6mnH-3Cnt-20171210_12-54-02220.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-8mxH-6mnH-2Cnt-20171210_12-54-02882.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-8mxH-6mnH-2Cnt-20171210_12-54-02166.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-8mxH-6mnH-1Cnt-20171210_12-54-01846.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-8mxH-6mnH-1Cnt-20171210_12-54-01787.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-8mxH-1mnH-3Cnt-20171210_12-54-01670.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-8mxH-1mnH-3Cnt-20171210_12-54-01379.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-8mxH-1mnH-2Cnt-20171210_12-54-01978.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-8mxH-1mnH-2Cnt-20171210_12-54-01528.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-8mxH-1mnH-1Cnt-20171210_12-54-0181.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-24mxP-8mxC-8mxH-1mnH-1Cnt-20171210_12-54-0174.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-10mxH-8mnH-3Cnt-20171210_12-53-52827.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-10mxH-8mnH-3Cnt-20171210_12-53-523.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-10mxH-8mnH-2Cnt-20171210_12-53-52736.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-10mxH-8mnH-2Cnt-20171210_12-53-52445.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-10mxH-8mnH-1Cnt-20171210_12-53-52972.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-10mxH-8mnH-1Cnt-20171210_12-53-52192.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-10mxH-1mnH-3Cnt-20171210_12-53-51853.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-10mxH-1mnH-3Cnt-20171210_12-53-51524.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-10mxH-1mnH-2Cnt-20171210_12-53-51604.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-10mxH-1mnH-2Cnt-20171210_12-53-51530.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-10mxH-1mnH-1Cnt-20171210_12-53-51711.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-10mxH-1mnH-1Cnt-20171210_12-53-51467.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-5mxH-4mnH-3Cnt-20171210_12-53-53997.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-5mxH-4mnH-3Cnt-20171210_12-53-53632.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-5mxH-4mnH-2Cnt-20171210_12-53-53238.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-5mxH-4mnH-2Cnt-20171210_12-53-53132.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-5mxH-4mnH-1Cnt-20171210_12-53-53435.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-5mxH-4mnH-1Cnt-20171210_12-53-53350.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-5mxH-1mnH-3Cnt-20171210_12-53-53643.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-5mxH-1mnH-3Cnt-20171210_12-53-53238.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-5mxH-1mnH-2Cnt-20171210_12-53-52737.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-5mxH-1mnH-2Cnt-20171210_12-53-52241.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-5mxH-1mnH-1Cnt-20171210_12-53-52417.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-10mxC-5mxH-1mnH-1Cnt-20171210_12-53-52178.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-8mnH-3Cnt-20171210_12-53-55645.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-8mnH-3Cnt-20171210_12-53-55599.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-8mnH-2Cnt-20171210_12-53-54897.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-8mnH-2Cnt-20171210_12-53-54392.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-8mnH-1Cnt-20171210_12-53-54927.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-8mnH-1Cnt-20171210_12-53-54759.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-3Cnt-20171210_12-53-54360.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-3Cnt-20171210_12-53-5424.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-2Cnt-20171210_12-53-54762.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-2Cnt-20171210_12-53-54206.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-1Cnt-20171210_12-53-53795.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-1Cnt-20171210_12-53-5353.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-5mxH-4mnH-3Cnt-20171210_12-53-56802.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-5mxH-4mnH-3Cnt-20171210_12-53-56313.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-5mxH-4mnH-2Cnt-20171210_12-53-55760.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-5mxH-4mnH-2Cnt-20171210_12-53-5562.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-5mxH-4mnH-1Cnt-20171210_12-53-55513.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-5mxH-4mnH-1Cnt-20171210_12-53-55308.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-5mxH-1mnH-3Cnt-20171210_12-53-55719.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-5mxH-1mnH-3Cnt-20171210_12-53-55159.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-5mxH-1mnH-2Cnt-20171210_12-53-55422.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-5mxH-1mnH-2Cnt-20171210_12-53-55168.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-5mxH-1mnH-1Cnt-20171210_12-53-55990.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-5mxH-1mnH-1Cnt-20171210_12-53-55637.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-5mxH-4mnH-3Cnt-20171210_12-53-47906.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-5mxH-4mnH-3Cnt-20171210_12-53-47293.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-5mxH-4mnH-2Cnt-20171210_12-53-47722.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-5mxH-4mnH-2Cnt-20171210_12-53-47596.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-5mxH-4mnH-1Cnt-20171210_12-53-47511.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-5mxH-4mnH-1Cnt-20171210_12-53-47345.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-5mxH-1mnH-3Cnt-20171210_12-53-47769.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-5mxH-1mnH-3Cnt-20171210_12-53-47135.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-5mxH-1mnH-2Cnt-20171210_12-53-47256.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-5mxH-1mnH-2Cnt-20171210_12-53-47175.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-5mxH-1mnH-1Cnt-20171210_12-53-46640.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-5mxH-1mnH-1Cnt-20171210_12-53-46102.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-2mxH-1mnH-3Cnt-20171210_12-53-48832.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-2mxH-1mnH-3Cnt-20171210_12-53-48783.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-2mxH-1mnH-3Cnt-20171210_12-53-48491.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-2mxH-1mnH-3Cnt-20171210_12-53-48296.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-2mxH-1mnH-2Cnt-20171210_12-53-48957.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-2mxH-1mnH-2Cnt-20171210_12-53-48639.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-2mxH-1mnH-2Cnt-20171210_12-53-48636.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-2mxH-1mnH-2Cnt-20171210_12-53-48609.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-2mxH-1mnH-1Cnt-20171210_12-53-48695.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-2mxH-1mnH-1Cnt-20171210_12-53-48569.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-2mxH-1mnH-1Cnt-20171210_12-53-48315.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-5mxC-2mxH-1mnH-1Cnt-20171210_12-53-4812.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-5mxH-4mnH-3Cnt-20171210_12-53-50774.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-5mxH-4mnH-3Cnt-20171210_12-53-50279.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-5mxH-4mnH-2Cnt-20171210_12-53-50951.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-5mxH-4mnH-2Cnt-20171210_12-53-5059.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-5mxH-4mnH-1Cnt-20171210_12-53-50375.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-5mxH-4mnH-1Cnt-20171210_12-53-49690.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-5mxH-1mnH-3Cnt-20171210_12-53-49759.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-5mxH-1mnH-3Cnt-20171210_12-53-49548.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-5mxH-1mnH-2Cnt-20171210_12-53-49554.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-5mxH-1mnH-2Cnt-20171210_12-53-49387.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-5mxH-1mnH-1Cnt-20171210_12-53-49884.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-5mxH-1mnH-1Cnt-20171210_12-53-4932.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-3Cnt-20171210_12-53-51891.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-3Cnt-20171210_12-53-51627.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-3Cnt-20171210_12-53-50687.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-3Cnt-20171210_12-53-50438.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-2Cnt-20171210_12-53-51804.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-2Cnt-20171210_12-53-51215.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-2Cnt-20171210_12-53-50592.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-2Cnt-20171210_12-53-50225.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-1Cnt-20171210_12-53-51342.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-1Cnt-20171210_12-53-50941.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-1Cnt-20171210_12-53-50893.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-1Cnt-20171210_12-53-50429.dat", logname, "SUCCESS", 1 );
var ofile = new IloOplOutputFile(logname, true);
ofile.writeln("{\"end\":\"end\"}]");
ofile.close();

def.end();
cplex.end();
src.end(); 
 
};