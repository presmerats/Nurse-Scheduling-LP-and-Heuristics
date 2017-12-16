/*********************************************
 * OPL 12.6.0.0 Model
 * Author: homero
 * Creation Date: 05/12/2017 at 16:48:44
 *********************************************/

 /*********************************************
 * OPL 12.6.0.0 Model
 * Author: Adrian Rodriguez Bazaga, Pau Rodriguez Esmerats
 * Creation Date: 09/11/2017 at 14:53:13
 *********************************************/

 
 main {


function myTest(def, cplex, filename, goal, showsol) {

 var ofile = new IloOplOutputFile("tests-model01-hfree.txt", true);
 
 var model = new IloOplModel(def,cplex);
 var data = new IloOplDataSource(filename);
 model.addDataSource(data);
 model.generate();
 cplex.epgap=0.01;
 if (cplex.solve() && goal == "SUCCESS") {
 	ofile.writeln("SUCCESS/SUCCESS ---------------------- ok: "+filename + " time: "+cplex.getSolvedTime()+" int vars: "+cplex.getNintVars());
 	ofile.writeln("                ---------------------- int vars: "+cplex.getNintVars());
 	ofile.writeln("                ---------------------- data: ")
 	ofile.writeln(model.printExternalData());
 	ofile.writeln("                ---------------------- sol: ")
 	ofile.writeln(model.printSolution());

 	if (showsol == "y")
 		model.printSolution();
} else if (!cplex.solve() && goal == "FAIL") {
 	ofile.writeln("FAIL/FAIL       ---------------------- ok: "+filename);
} else {
	ofile.writeln("FAIL/SUCCESS    ------------------- ERROR: "+filename);
} 	

 ofile.close();
 data.end();
 model.end();
  return true;
}




var src = new IloOplModelSource("model01-hfree.mod");
var def = new IloOplModelDefinition(src);
var cplex = new IloCplex();




myTest(def, cplex,"test_c1.dat","SUCCESS" );

myTest(def, cplex,"test_c2.dat","SUCCESS" );
myTest(def, cplex,"test_c3.dat","SUCCESS" );
myTest(def, cplex,"test_c4.dat","SUCCESS" );
myTest(def, cplex,"test_c5.dat","SUCCESS" );
myTest(def, cplex,"test_c6.dat","SUCCESS" );

//myTest(def, cplex,"x_15_0.dat","SUCCESS" );
myTest(def, cplex,"x_16_0.dat","SUCCESS" );
/*
myTest(def, cplex,"x_16_1.dat","SUCCESS" );
myTest(def, cplex,"x_16_2.dat","SUCCESS" );
myTest(def, cplex,"x_16_3.dat","SUCCESS" );
myTest(def, cplex,"x_16_4.dat","SUCCESS" );
myTest(def, cplex,"x_16_5.dat","SUCCESS" );
myTest(def, cplex,"x_16_6.dat","SUCCESS" );
myTest(def, cplex,"x_16_7.dat","SUCCESS" );
myTest(def, cplex,"x_16_8.dat","SUCCESS" );
myTest(def, cplex,"x_16_9.dat","SUCCESS" );


myTest(def, cplex,"i-manual-30-962-740-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-955-735-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-949-730-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-942-725-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-936-720-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-929-715-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-923-710-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-916-705-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-910-700-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-961-745-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-954-740-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-948-735-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-941-730-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-935-725-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-928-720-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-922-715-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-915-710-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-909-705-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-903-700-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-953-745-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-947-740-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-940-735-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-934-730-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-928-725-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-921-720-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-915-715-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-908-710-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-902-705-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-896-700-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-946-745-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-939-740-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-933-735-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-927-730-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-920-725-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-914-720-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-908-715-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-901-710-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-895-705-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-889-700-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-938-745-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-932-740-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-926-735-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-919-730-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-913-725-20171201_05-00-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-907-720-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-900-715-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-894-710-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-888-705-20171201_05-00-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-882-700-20171201_05-00-18.dat","SUCCESS" );
*/
def.end();
cplex.end();
src.end(); 
 
};