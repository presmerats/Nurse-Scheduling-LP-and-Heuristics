 /*********************************************
 * OPL 12.6.0.0 Model
 * Author: Adrian Rodriguez Bazaga, Pau Rodriguez Esmerats
 * Creation Date: 09/11/2017 at 14:53:13
 *********************************************/

 
 main {


function myTest(def, cplex, filename, goal, objf, showsol) {

 var ofile = new IloOplOutputFile("log-tests-model01-hfree.txt", true);
 
 var model = new IloOplModel(def,cplex);
 var data = new IloOplDataSource(filename);
 model.addDataSource(data);
 model.generate();
 cplex.epgap=0.01;
 if (cplex.solve() && goal == "SUCCESS" && cplex.getObjValue() == objf) {
 	ofile.writeln("SUCCESS/SUCCESS ---------------------- ok: "+filename + " time: "+cplex.getSolvedTime()+" int vars: "+cplex.getNintVars());

} else if (!cplex.solve() && goal == "FAIL") {
 	ofile.writeln("FAIL/FAIL       ---------------------- ok: "+filename);
} else {
	ofile.writeln("FAIL/SUCCESS    ------------------- ERROR: "+filename+" objfunc="+cplex.getObjValue()+" != "+objf);
} 	

 	ofile.writeln("                --- int vars: "+cplex.getNintVars());
 	//ofile.writeln("                --- lower bound: "+cplex.getLb());
 	ofile.writeln("                --- Gap: "+cplex.getMIPRelativeGap());
 	ofile.writeln("                --- Obj Func: "+cplex.getObjValue());
 	ofile.writeln("                --- MIP?: "+cplex.isMIP());
 	ofile.writeln("                --- data: ")
 	ofile.writeln(model.printExternalData());
 	ofile.writeln("                --- sol: ")
 	ofile.writeln(model.printSolution());

 	//if (showsol == "y")
 	//	model.printSolution();

 ofile.close();
 data.end();
 model.end();
  return true;
}




var src = new IloOplModelSource("model01-hfree.mod");
var def = new IloOplModelDefinition(src);
var cplex = new IloCplex();




myTest(def, cplex,"test_c1.dat","SUCCESS" ,1);
myTest(def, cplex,"test_c2.dat","SUCCESS" ,1);
myTest(def, cplex,"test_c3.dat","SUCCESS" ,2);
myTest(def, cplex,"test_c4.dat","SUCCESS" ,1);
myTest(def, cplex,"test_c5.dat","SUCCESS" ,2);
myTest(def, cplex,"test_c5_b.dat","SUCCESS" ,2);
myTest(def, cplex,"test_c6.dat","SUCCESS" ,1);

def.end();
cplex.end();
src.end(); 
 
};