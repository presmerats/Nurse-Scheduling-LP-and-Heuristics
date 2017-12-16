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





myTest(def, cplex,"i-manual-30-643-495-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-637-490-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-630-485-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-624-480-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-617-475-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-611-470-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-604-465-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-598-460-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-591-455-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-585-450-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-578-445-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-572-440-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-565-435-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-559-430-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-552-425-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-546-420-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-539-415-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-533-410-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-526-405-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-520-400-20171201_09-09-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-638-495-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-632-490-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-625-485-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-619-480-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-612-475-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-606-470-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-599-465-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-593-460-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-586-455-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-580-450-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-574-445-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-567-440-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-561-435-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-554-430-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-548-425-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-541-420-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-535-415-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-528-410-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-522-405-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-516-400-20171201_09-09-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-633-495-20171201_09-09-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-627-490-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-620-485-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-614-480-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-608-475-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-601-470-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-595-465-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-588-460-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-582-455-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-576-450-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-569-445-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-563-440-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-556-435-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-550-430-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-544-425-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-537-420-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-531-415-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-524-410-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-518-405-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-512-400-20171201_09-09-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-628-495-20171201_09-09-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-622-490-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-615-485-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-609-480-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-603-475-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-596-470-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-590-465-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-584-460-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-577-455-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-571-450-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-565-445-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-558-440-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-552-435-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-546-430-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-539-425-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-533-420-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-527-415-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-520-410-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-514-405-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-508-400-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-623-495-20171201_09-09-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-617-490-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-611-485-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-604-480-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-598-475-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-592-470-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-585-465-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-579-460-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-573-455-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-567-450-20171201_09-09-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-560-445-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-554-440-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-548-435-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-541-430-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-535-425-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-529-420-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-522-415-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-516-410-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-510-405-20171201_09-09-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-504-400-20171201_09-09-14.dat","SUCCESS" );
 
def.end();
cplex.end();
src.end(); 
 
};