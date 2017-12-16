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
myTest(def, cplex,"i-manual-20-228-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-216-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-204-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-192-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-180-150-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-168-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-156-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-144-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-132-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-120-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-226-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-214-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-202-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-190-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-178-150-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-166-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-119-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-224-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-212-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-200-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-188-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-177-150-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-165-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-154-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-153-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-142-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-141-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-130-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-118-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-222-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-210-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-187-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-175-150-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-152-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-140-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-129-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-117-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-220-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-208-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-198-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-197-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-185-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-174-150-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-163-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-162-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-139-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-128-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-116-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-218-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-207-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-195-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-184-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-172-150-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-161-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-150-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-149-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-138-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-127-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-126-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-115-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-216-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-205-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-193-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-182-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-171-150-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-159-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-148-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-125-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-114-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-214-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-203-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-192-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-169-150-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-158-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-136-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-124-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-113-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-212-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-201-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-190-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-180-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-179-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-168-150-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-146-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-145-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-135-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-134-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-123-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-112-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-210-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-199-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-188-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-177-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-166-150-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-156-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-155-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-144-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-133-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-122-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-111-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-209-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-198-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-187-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-176-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-165-150-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-154-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-143-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-132-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-121-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-10-110-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-9-207-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-9-196-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-9-185-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-9-174-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-9-163-150-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-9-152-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-9-109-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-8-205-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-8-194-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-8-183-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-8-162-150-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-8-151-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-8-141-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-8-140-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-8-130-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-8-119-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-8-108-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-7-203-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-7-192-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-7-172-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-7-171-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-7-160-150-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-7-139-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-7-129-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-7-128-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-7-118-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-7-107-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-6-201-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-6-190-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-6-181-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-6-180-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-6-169-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-6-159-150-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-6-149-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-6-148-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-6-127-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-6-117-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-6-106-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-5-199-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-5-189-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-5-178-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-5-168-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-5-157-150-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-5-147-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-5-137-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-5-136-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-5-126-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-5-116-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-5-115-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-5-105-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-4-197-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-4-187-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-4-176-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-4-166-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-4-156-150-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-4-145-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-4-135-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-4-114-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-4-104-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-3-195-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-3-185-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-3-175-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-3-154-150-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-3-144-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-3-124-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-3-113-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-3-103-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-2-193-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-2-183-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-2-173-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-2-164-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-2-163-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-2-153-150-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-2-133-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-2-132-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-2-123-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-2-122-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-2-112-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-2-102-100-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-1-191-190-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-1-181-180-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-1-171-170-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-1-161-160-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-1-151-150-20171121_23-07-30.dat","SUCCESS" );
myTest(def, cplex,"i-manual-1-142-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-1-141-140-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-1-131-130-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-1-121-120-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-1-111-110-20171121_23-07-29.dat","SUCCESS" );
myTest(def, cplex,"i-manual-1-101-100-20171121_23-07-29.dat","SUCCESS" );
 


 def.end();
 cplex.end();
 src.end(); 
 
};