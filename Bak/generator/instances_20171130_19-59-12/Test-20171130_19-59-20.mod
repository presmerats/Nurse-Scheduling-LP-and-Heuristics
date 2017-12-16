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





myTest(def, cplex,"i-manual-20-1194-995-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1188-990-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1182-985-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1176-980-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1170-975-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1164-970-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1158-965-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1152-960-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1146-955-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1140-950-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1134-945-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1128-940-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1122-935-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1116-930-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1110-925-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1104-920-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1098-915-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1092-910-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1086-905-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-20-1080-900-20171130_19-59-12.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1184-995-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1178-990-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1172-985-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1166-980-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1160-975-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1154-970-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1148-965-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1142-960-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1136-955-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1130-950-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1124-945-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1118-940-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1112-935-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1106-930-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1100-925-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1094-920-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1088-915-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1082-910-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1076-905-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-19-1071-900-20171130_19-59-12.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1174-995-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1168-990-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1162-985-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1156-980-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1150-975-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1144-970-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1138-965-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1132-960-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1126-955-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1121-950-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1115-945-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1109-940-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1103-935-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1097-930-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1091-925-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1085-920-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1079-915-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1073-910-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1067-905-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-18-1062-900-20171130_19-59-12.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1164-995-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1158-990-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1152-985-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1146-980-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1140-975-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1134-970-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1129-965-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1123-960-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1117-955-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1111-950-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1105-945-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1099-940-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1093-935-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1088-930-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1082-925-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1076-920-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1070-915-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1064-910-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1058-905-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-17-1053-900-20171130_19-59-12.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1154-995-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1148-990-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1142-985-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1136-980-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1131-975-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1125-970-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1119-965-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1113-960-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1107-955-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1102-950-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1096-945-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1090-940-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1084-935-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1078-930-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1073-925-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1067-920-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1061-915-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1055-910-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1049-905-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-16-1044-900-20171130_19-59-12.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1144-995-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1138-990-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1132-985-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1127-980-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1121-975-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1115-970-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1109-965-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1104-960-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1098-955-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1092-950-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1086-945-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1081-940-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1075-935-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1069-930-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1063-925-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1058-920-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1052-915-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1046-910-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1040-905-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-15-1035-900-20171130_19-59-12.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1134-995-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1128-990-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1122-985-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1117-980-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1111-975-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1105-970-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1100-965-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1094-960-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1088-955-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1083-950-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1077-945-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1071-940-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1065-935-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1060-930-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1054-925-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1048-920-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1043-915-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1037-910-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1031-905-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-14-1026-900-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1124-995-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1118-990-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1113-985-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1107-980-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1101-975-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1096-970-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1090-965-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1084-960-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1079-955-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1073-950-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1067-945-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1062-940-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1056-935-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1050-930-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1045-925-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1039-920-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1033-915-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1028-910-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1022-905-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-13-1017-900-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1114-995-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1108-990-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1103-985-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1097-980-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1092-975-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1086-970-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1080-965-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1075-960-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1069-955-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1064-950-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1058-945-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1052-940-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1047-935-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1041-930-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1036-925-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1030-920-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1024-915-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1019-910-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1013-905-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-12-1008-900-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1104-995-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1098-990-20171130_19-59-20.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1093-985-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1087-980-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1082-975-20171130_19-59-19.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1076-970-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1071-965-20171130_19-59-18.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1065-960-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1060-955-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1054-950-20171130_19-59-17.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1048-945-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1043-940-20171130_19-59-16.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1037-935-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1032-930-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1026-925-20171130_19-59-15.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1021-920-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1015-915-20171130_19-59-14.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1010-910-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-1004-905-20171130_19-59-13.dat","SUCCESS" );
myTest(def, cplex,"i-manual-11-999-900-20171130_19-59-13.dat","SUCCESS" );
 
def.end();
cplex.end();
src.end(); 
 
};