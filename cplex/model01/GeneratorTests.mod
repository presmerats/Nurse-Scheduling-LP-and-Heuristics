/*********************************************
 * OPL 12.6.0.0 Model
 * Author: homero
 * Creation Date: 14/11/2017 at 10:12:51
 *********************************************/
/*********************************************
 * OPL 12.6.0.0 Model
 * Author: homero
 * Creation Date: 09/11/2017 at 14:53:13
 *********************************************/

 
 main {


function myTest(def, cplex, filename, goal, showsol) {

 var model = new IloOplModel(def,cplex);
 var data = new IloOplDataSource(filename);
 model.addDataSource(data);
 model.generate();
 cplex.epgap=0.01;
 if (cplex.solve() && goal == "SUCCESS") {
 	writeln("SUCCESS/SUCCESS ---------------------- ok: "+filename + " time: "+cplex.getSolvedTime());
 	if (showsol == "y")
 		model.printSolution();
} else if (!cplex.solve() && goal == "FAIL") {
 	writeln("FAIL/FAIL       ---------------------- ok: "+filename);
} else {
	writeln("FAIL/SUCCESS    ------------------- ERROR: "+filename);
} 	
 data.end();
 model.end();
  return true;
}


 var src = new IloOplModelSource("model01.mod");
 var def = new IloOplModelDefinition(src);
 var cplex = new IloCplex();
 
myTest(def, cplex,"instance-manual-100-20171114_10-07-52.dat","SUCCESS" );
myTest(def, cplex,"instance-100-20171108_14-40-00.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-100-20171114_09-47-46.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-100-20171114_10-12-18.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-100-20171114_10-11-08.dat","SUCCESS" );
myTest(def, cplex,"instance-distr-100-20171114_09-45-09.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-100-20171114_10-06-25.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-100-20171114_10-06-38.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-100-20171114_09-45-09.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-100-20171114_10-11-24.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-100-20171114_09-48-26.dat","SUCCESS" );
myTest(def, cplex,"instance-distr-100-20171114_09-44-18.dat","SUCCESS" );
myTest(def, cplex,"instance-distr-100-20171114_09-45-01.dat","SUCCESS" );
myTest(def, cplex,"instance-100-20171108_14-40-15.dat","SUCCESS" );
myTest(def, cplex,"datafile.dat","SUCCESS" );
 
 def.end();
 cplex.end();
 src.end(); 
 
};