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
 cplex.epgap=0.01;
 // 540000.0 1h
 // 245000.0 30m
 // 122500.0 15m
 // 061250.0 7m
 //   9000.0 1m
 cplex.DetTiLim=122500.0;
 //model.setParam(IloCplex.Param.tune.DetTimeLimit,10.0);
 
 //try {
  
  ofile.writeln("\"expected_output\" : \""+goal+"\",");
  ofile.writeln("\"computed_output\" : \""+cplex.solve()+"\",");
  ofile.writeln("\"desired_objfunc\" : \""+objf+"\",");
	
	if (cplex.solve()){
	 	
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







myTest(def, cplex,"test_c1.dat",logname,"SUCCESS" ,1);
myTest(def, cplex,"test_c2.dat",logname,"SUCCESS" ,1);
myTest(def, cplex,"test_c3.dat",logname,"SUCCESS" ,2);
myTest(def, cplex,"test_c4.dat",logname,"SUCCESS" ,2);
myTest(def, cplex,"test_c5.dat",logname,"SUCCESS" ,2);
myTest(def, cplex,"test_c5_b.dat",logname,"SUCCESS" ,1);
myTest(def, cplex,"test_c6.dat",logname,"SUCCESS" ,2);

myTest(def, cplex,"test_basicTest-maxConsec01.dat",logname,"FAIL" ,1);
myTest(def, cplex,"test_basicTest-maxConsec02.dat",logname,"SUCCESS" ,1);

myTest(def, cplex,"test_basicTest-maxHours_2.dat",logname,"SUCCESS" ,2);
myTest(def, cplex,"test_basicTest-maxHours_3.dat",logname,"SUCCESS" ,2);
myTest(def, cplex,"test_basicTest-maxHours_4.dat",logname,"SUCCESS" ,2);
myTest(def, cplex,"test_basicTest-maxHours_5.dat",logname,"SUCCESS" ,1);
myTest(def, cplex,"test_basicTest-maxHours01.dat",logname,"FAIL" ,1);
myTest(def, cplex,"test_basicTest-maxHours02.dat",logname,"SUCCESS" ,1);

myTest(def, cplex,"test_basicTest-maxPresence01.dat",logname,"FAIL" ,1);
myTest(def, cplex,"test_basicTest-maxPresence02.dat",logname,"SUCCESS" ,2);
myTest(def, cplex,"test_basicTest-maxPresence03.dat",logname,"FAIL" ,1);
myTest(def, cplex,"test_basicTest-maxRest01.dat",logname,"SUCCESS" ,1);
myTest(def, cplex,"test_basicTest-maxRest02.dat",logname,"SUCCESS" ,2);
myTest(def, cplex,"test_basicTest-maxRest03.dat",logname,"SUCCESS" ,1);
myTest(def, cplex,"test_basicTest-maxRest04.dat",logname,"SUCCESS" ,4);
myTest(def, cplex,"test_basicTest-maxRest05.dat",logname,"SUCCESS" ,3);
myTest(def, cplex,"test_basicTest-maxRest06.dat",logname,"SUCCESS" ,1);
myTest(def, cplex,"test_basicTest-minHours01.dat",logname,"SUCCESS" ,1);
myTest(def, cplex,"test_basicTest-minHours02.dat",logname,"SUCCESS" ,1);

myTest(def, cplex,"test_basicTest-manual-solution01.dat",logname,"SUCCESS" ,4);
myTest(def, cplex,"test_basicTest-manual-solution02.dat",logname,"FAIL" ,5);
myTest(def, cplex,"test_basicTest-manual-solution03.dat",logname,"SUCCESS" ,5);


var ofile = new IloOplOutputFile(logname, true);
ofile.writeln("{\"end\":\"end\"}]");
ofile.close();

def.end();
cplex.end();
src.end(); 
 
};