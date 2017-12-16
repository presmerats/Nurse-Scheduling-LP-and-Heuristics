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





myTest(def, cplex,"i-manual-30-383-295-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-377-290-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-370-285-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-364-280-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-357-275-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-351-270-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-344-265-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-338-260-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-331-255-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-325-250-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-318-245-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-312-240-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-305-235-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-299-230-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-292-225-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-286-220-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-279-215-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-273-210-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-266-205-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-30-260-200-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-380-295-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-374-290-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-367-285-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-361-280-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-354-275-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-348-270-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-341-265-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-335-260-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-328-255-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-322-250-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-316-245-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-309-240-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-303-235-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-296-230-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-290-225-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-283-220-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-277-215-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-270-210-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-264-205-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-29-258-200-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-377-295-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-371-290-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-364-285-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-358-280-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-352-275-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-345-270-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-339-265-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-332-260-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-326-255-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-320-250-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-313-245-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-307-240-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-300-235-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-294-230-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-288-225-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-281-220-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-275-215-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-268-210-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-262-205-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-28-256-200-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-374-295-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-368-290-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-361-285-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-355-280-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-349-275-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-342-270-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-336-265-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-330-260-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-323-255-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-317-250-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-311-245-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-304-240-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-298-235-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-292-230-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-285-225-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-279-220-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-273-215-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-266-210-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-260-205-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-27-254-200-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-371-295-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-365-290-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-359-285-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-352-280-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-346-275-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-340-270-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-333-265-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-327-260-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-321-255-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-315-250-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-308-245-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-302-240-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-296-235-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-289-230-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-283-225-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-277-220-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-270-215-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-264-210-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-258-205-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-26-252-200-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-368-295-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-362-290-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-356-285-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-350-280-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-343-275-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-337-270-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-331-265-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-325-260-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-318-255-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-312-250-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-306-245-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-300-240-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-293-235-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-287-230-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-281-225-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-275-220-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-268-215-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-262-210-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-256-205-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-25-250-200-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-365-295-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-359-290-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-353-285-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-347-280-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-341-275-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-334-270-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-328-265-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-322-260-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-316-255-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-310-250-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-303-245-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-297-240-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-291-235-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-285-230-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-279-225-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-272-220-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-266-215-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-260-210-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-254-205-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-24-248-200-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-362-295-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-356-290-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-350-285-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-344-280-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-338-275-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-332-270-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-325-265-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-319-260-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-313-255-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-307-250-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-301-245-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-295-240-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-289-235-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-282-230-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-276-225-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-270-220-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-264-215-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-258-210-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-252-205-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-23-246-200-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-359-295-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-353-290-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-347-285-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-341-280-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-335-275-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-329-270-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-323-265-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-317-260-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-311-255-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-305-250-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-298-245-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-292-240-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-286-235-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-280-230-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-274-225-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-268-220-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-262-215-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-256-210-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-250-205-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-22-244-200-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-356-295-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-350-290-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-344-285-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-338-280-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-332-275-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-326-270-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-320-265-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-314-260-20171130_21-37-55.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-308-255-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-302-250-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-296-245-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-290-240-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-284-235-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-278-230-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-272-225-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-266-220-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-260-215-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-254-210-20171130_21-37-54.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-248-205-20171130_21-37-53.dat","SUCCESS" );
myTest(def, cplex,"i-manual-21-242-200-20171130_21-37-53.dat","SUCCESS" );
 
def.end();
cplex.end();
src.end(); 
 
};