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
 
 myTest(def, cplex,"instance-manual-123-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-226-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-199-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-131-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-163-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-174-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-143-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-181-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-190-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-104-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-166-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-201-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-147-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-151-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-144-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-179-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-162-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-150-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-129-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-112-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-159-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-152-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-117-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-111-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-153-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-203-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-126-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-158-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-154-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-191-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-156-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-119-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-156-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-115-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-142-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-173-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-142-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-136-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-140-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-183-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-160-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-122-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-195-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-192-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-207-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-155-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-197-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-171-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-149-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-110-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-120-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-116-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-118-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-133-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-141-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-204-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-159-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-138-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-220-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-134-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-194-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-224-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-228-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-141-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-113-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-103-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-161-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-109-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-218-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-216-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-180-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-108-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-107-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-166-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-125-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-162-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-202-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-163-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-172-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-184-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-146-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-175-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-198-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-178-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-157-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-182-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-101-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-187-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-177-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-132-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-208-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-200-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-144-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-102-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-165-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-106-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-185-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-168-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-153-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-176-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-105-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-165-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-189-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-196-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-145-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-214-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-188-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-164-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-114-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-135-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-168-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-209-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-169-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-139-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-205-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-151-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-222-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-121-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-212-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-154-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-161-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-127-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-210-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-145-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-137-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-130-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-128-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-124-20171121_11-28-44.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-193-20171121_11-28-45.dat","SUCCESS" );
myTest(def, cplex,"instance-manual-148-20171121_11-28-44.dat","SUCCESS" );
 
 def.end();
 cplex.end();
 src.end(); 
 
};