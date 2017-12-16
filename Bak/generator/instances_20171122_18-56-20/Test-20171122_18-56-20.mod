/*********************************************
 * OPL 12.6.0.0 Model
 * Author: Adrian Rodriguez Bazaga, Pau Rodriguez Esmerats
 * Creation Date: 09/11/2017 at 14:53:13
 *********************************************/

 
 main {


function myTest(def, cplex, filename, goal, showsol) {

 var ofile = new IloOplOutputFile("modelRun.txt", true);
 
 var model = new IloOplModel(def,cplex);
 var data = new IloOplDataSource(filename);
 model.addDataSource(data);
 model.generate();
 cplex.epgap=0.01;
 if (cplex.solve() && goal == "SUCCESS") {
 	ofile.writeln("SUCCESS/SUCCESS ---------------------- ok: "+filename + " time: "+cplex.getSolvedTime());
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

// clean log file
var ofile = new IloOplOutputFile("modelRun.txt");
writeln("");
ofile.close();


 var src = new IloOplModelSource("model01.mod");
 var def = new IloOplModelDefinition(src);
 var cplex = new IloCplex();
myTest(def, cplex,"i-manual-20-120-100-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-114-95-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-108-90-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-102-85-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-96-80-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-90-75-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-84-70-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-78-65-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-72-60-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-66-55-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-60-50-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-54-45-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-48-40-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-42-35-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-36-30-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-30-25-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-24-20-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-119-100-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-113-95-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-107-90-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-101-85-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-95-80-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-89-75-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-83-70-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-118-100-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-112-95-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-106-90-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-100-85-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-94-80-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-77-65-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-71-60-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-65-55-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-59-50-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-53-45-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-47-40-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-117-100-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-111-95-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-105-90-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-88-75-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-82-70-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-76-65-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-70-60-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-41-35-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-35-30-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-116-100-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-110-95-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-104-90-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-99-85-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-93-80-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-87-75-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-81-70-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-64-55-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-58-50-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-52-45-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-29-25-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-115-100-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-109-95-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-98-85-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-92-80-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-86-75-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-75-65-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-69-60-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-63-55-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-46-40-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-23-20-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-114-100-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-108-95-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-103-90-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-97-85-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-91-80-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-80-70-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-74-65-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-57-50-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-40-35-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-113-100-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-107-95-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-102-90-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-96-85-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-85-75-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-79-70-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-68-60-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-62-55-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-51-45-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-34-30-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-112-100-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-106-95-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-101-90-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-95-85-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-90-80-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-84-75-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-73-65-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-67-60-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-56-50-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-45-40-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-28-25-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-111-100-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-105-95-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-100-90-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-94-85-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-89-80-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-83-75-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-78-70-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-72-65-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-61-55-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-50-45-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-39-35-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-99-90-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-88-80-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-77-70-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-66-60-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-55-50-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-44-40-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-33-30-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-22-20-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-9-49-45-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-9-38-35-20171122_18-56-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-8-27-25-20171122_18-56-20.dat","SUCCESS" );
 


 def.end();
 cplex.end();
 src.end(); 
 
};