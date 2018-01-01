/*********************************************
* Author: Adrian Rodriguez Bazaga, Pau Rodriguez Esmerats
*********************************************/

 
	main {
		function constraintTest(def, cplex, filename, goal, objf, showsol) {
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
				if(cplex.solve()){
					ofile.writeln("FAIL/SUCCESS    ------------------- ERROR: "+filename+" objfunc="+cplex.getObjValue()+" != "+objf);
				} else {
					ofile.writeln("FAIL/SUCCESS    ------------------- ERROR: "+filename+" objfunc=UNSOLVED != "+objf);
				}	
			} 	

			if (cplex.solve()){
				ofile.writeln("                --- int vars: "+cplex.getNintVars());
				//ofile.writeln("                --- lower bound: "+cplex.getLb());
				ofile.writeln("                --- Gap: "+cplex.getMIPRelativeGap());
				ofile.writeln("                --- Obj Func: "+cplex.getObjValue());
				ofile.writeln("                --- MIP?: "+cplex.isMIP());
				ofile.writeln("                --- data: ")
				ofile.writeln(model.printExternalData());
				ofile.writeln("                --- sol: ")
				ofile.writeln(model.printSolution());
			} else {
				ofile.writeln("                --- data: ")
				ofile.writeln(model.printExternalData());	
			}	 	

			ofile.close();
			data.end();
			model.end();
			return true;
		}




		var src = new IloOplModelSource("model01-hfree.mod");
		var def = new IloOplModelDefinition(src);
		var cplex = new IloCplex();

		constraintTest(def, cplex,"test_c1.dat","SUCCESS" ,1);
		constraintTest(def, cplex,"test_c2.dat","SUCCESS" ,1);
		constraintTest(def, cplex,"test_c3.dat","SUCCESS" ,2);
		constraintTest(def, cplex,"test_c4.dat","SUCCESS" ,2);
		constraintTest(def, cplex,"test_c5.dat","SUCCESS" ,2);
		constraintTest(def, cplex,"test_c5_b.dat","SUCCESS" ,1);
		constraintTest(def, cplex,"test_c6.dat","SUCCESS" ,2);

		constraintTest(def, cplex,"test_basicTest-maxConsec01.dat","FAIL" ,1);
		constraintTest(def, cplex,"test_basicTest-maxConsec02.dat","SUCCESS" ,1);

		constraintTest(def, cplex,"test_basicTest-maxHours_2.dat","SUCCESS" ,2);
		constraintTest(def, cplex,"test_basicTest-maxHours_3.dat","SUCCESS" ,2);
		constraintTest(def, cplex,"test_basicTest-maxHours_4.dat","SUCCESS" ,2);
		constraintTest(def, cplex,"test_basicTest-maxHours_5.dat","SUCCESS" ,1);
		constraintTest(def, cplex,"test_basicTest-maxHours01.dat","FAIL" ,1);
		constraintTest(def, cplex,"test_basicTest-maxHours02.dat","SUCCESS" ,1);

		constraintTest(def, cplex,"test_basicTest-maxPresence01.dat","FAIL" ,1);
		constraintTest(def, cplex,"test_basicTest-maxPresence02.dat","SUCCESS" ,2);
		constraintTest(def, cplex,"test_basicTest-maxPresence03.dat","FAIL" ,1);
		constraintTest(def, cplex,"test_basicTest-maxRest01.dat","SUCCESS" ,1);
		constraintTest(def, cplex,"test_basicTest-maxRest02.dat","SUCCESS" ,2);
		constraintTest(def, cplex,"test_basicTest-maxRest03.dat","SUCCESS" ,1);
		constraintTest(def, cplex,"test_basicTest-maxRest04.dat","SUCCESS" ,4);
		constraintTest(def, cplex,"test_basicTest-maxRest05.dat","SUCCESS" ,3);
		constraintTest(def, cplex,"test_basicTest-maxRest06.dat","SUCCESS" ,1);
		constraintTest(def, cplex,"test_basicTest-minHours01.dat","SUCCESS" ,1);
		constraintTest(def, cplex,"test_basicTest-minHours02.dat","SUCCESS" ,1);

		constraintTest(def, cplex,"test_basicTest-manual-solution01.dat","SUCCESS" ,4);
		constraintTest(def, cplex,"test_basicTest-manual-solution02.dat","FAIL" ,5);
		constraintTest(def, cplex,"test_basicTest-manual-solution03.dat","SUCCESS" ,5);

		def.end();
		cplex.end();
		src.end(); 
};