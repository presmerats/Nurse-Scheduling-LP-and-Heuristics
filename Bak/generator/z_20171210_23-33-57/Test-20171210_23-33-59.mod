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

function myTest(def, cplex, filename, logname, tilim,  goal, objf,  showsol) {

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
 cplex.TiLim=tilim;
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

var logname = "log-i-search02-300-"+cplex.getCplexTime()+".txt"
var ofile = new IloOplOutputFile(logname, true);
ofile.writeln("[");
ofile.close();

var tilim = 300.0;






myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-9mnH-4Cnt-20171210_23-33-58231.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-9mnH-4Cnt-20171210_23-33-58173.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-9mnH-3Cnt-20171210_23-33-58853.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-9mnH-3Cnt-20171210_23-33-58250.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-9mnH-2Cnt-20171210_23-33-58914.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-9mnH-2Cnt-20171210_23-33-58138.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-9mnH-1Cnt-20171210_23-33-58768.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-9mnH-1Cnt-20171210_23-33-58646.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-9mnH-0Cnt-20171210_23-33-58151.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-9mnH-0Cnt-20171210_23-33-5866.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-4mnH-4Cnt-20171210_23-33-59919.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-4mnH-4Cnt-20171210_23-33-59718.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-4mnH-3Cnt-20171210_23-33-59703.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-4mnH-3Cnt-20171210_23-33-59372.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-4mnH-2Cnt-20171210_23-33-58769.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-4mnH-2Cnt-20171210_23-33-5923.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-4mnH-1Cnt-20171210_23-33-58987.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-4mnH-1Cnt-20171210_23-33-58660.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-4mnH-0Cnt-20171210_23-33-58429.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-4mnH-0Cnt-20171210_23-33-58121.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-4Cnt-20171210_23-33-58769.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-4Cnt-20171210_23-33-58568.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-3Cnt-20171210_23-33-58464.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-3Cnt-20171210_23-33-5862.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-2Cnt-20171210_23-33-57720.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-2Cnt-20171210_23-33-57502.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-1Cnt-20171210_23-33-57503.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-1Cnt-20171210_23-33-57217.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-0Cnt-20171210_23-33-57212.dat", logname, tilim,  "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-5mxC-10mxH-1mnH-0Cnt-20171210_23-33-57106.dat", logname, tilim,  "SUCCESS", 1 );
var ofile = new IloOplOutputFile(logname, true);
ofile.writeln("{\"end\":\"end\"}]");
ofile.close();

def.end();
cplex.end();
src.end(); 
 
};