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






myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-23-35.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-23-34.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-23-33.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-23-31.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-23-30.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-23-29.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-23-27.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-23-26.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-23-33.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-23-29.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-23-26.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-23-33.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-23-32.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-23-31.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-23-29.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-23-28.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-23-26.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-23-25.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-23-31.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-23-28.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-23-27.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-23-25.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-23-24.dat", logname, "SUCCESS", 1 );
var ofile = new IloOplOutputFile(logname, true);
ofile.writeln("{\"end\":\"end\"}]");
ofile.close();

def.end();
cplex.end();
src.end(); 
 
};