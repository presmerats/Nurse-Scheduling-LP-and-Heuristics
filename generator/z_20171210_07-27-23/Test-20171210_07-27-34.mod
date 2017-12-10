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






myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-34871.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-34738.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-34685.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-34470.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-34411.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-34382.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-34336.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-33967.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-33908.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-33775.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-33517.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-33251.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-33175.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32919.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32698.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-29869.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-29824.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-29738.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-29527.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-29510.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-29300.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-28791.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-28522.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-28516.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-28477.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-28335.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-28252.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-28248.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-28172.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-28101.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25999.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25900.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25843.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25782.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25770.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25754.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25720.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25503.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25400.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25314.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25281.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25271.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-25147.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-2563.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-160-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-2547.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32839.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32833.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32815.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32808.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32779.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32687.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32609.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32595.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32457.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32405.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32367.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32275.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32270.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32254.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32203.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-28940.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-28715.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-28623.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27853.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27650.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27574.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27478.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27389.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27383.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27353.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27202.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27127.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-2753.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-2719.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24981.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24932.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24908.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24828.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24820.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24649.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24377.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24332.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24264.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24262.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24224.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24178.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24130.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-2471.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-60-64-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-2438.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32381.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-31677.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-31565.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-31488.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-31441.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-31171.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-31151.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-30631.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-30359.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-30235.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-30189.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-30105.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-3154.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-3088.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-3031.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27753.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27724.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27478.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27323.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-27313.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26906.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26876.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26868.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26829.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26791.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26783.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26771.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26747.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26323.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-2648.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24995.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24883.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24878.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24747.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24736.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24652.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24586.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24563.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24446.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24433.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24215.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-24211.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23469.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-2468.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-120-100-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-243.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-30983.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-30714.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-29859.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-29732.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-29709.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-29676.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-29675.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-29673.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-29649.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-29566.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-29514.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-29297.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-29283.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-29126.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-2947.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26867.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26780.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26700.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26478.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26410.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-26321.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-25911.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-25724.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-25642.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-25517.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-25496.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-25435.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-25423.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-25326.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-18h-12mxP-6mxC-8mxH-2mnH-20171210_07-27-25325.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23824.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23771.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23672.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23660.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23635.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23526.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23470.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23436.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23417.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23406.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23382.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23373.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23336.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23230.dat", logname, "SUCCESS", 1 );
myTest(def, cplex,"i-ng-20-48-40-12h-8mxP-3mxC-5mxH-2mnH-20171210_07-27-23218.dat", logname, "SUCCESS", 1 );
var ofile = new IloOplOutputFile(logname, true);
ofile.writeln("{\"end\":\"end\"}]");
ofile.close();

def.end();
cplex.end();
src.end(); 
 
};