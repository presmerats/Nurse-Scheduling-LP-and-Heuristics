/*********************************************
 * OPL 12.6.0.0 Model
 * Author: homero
 * Creation Date: 05/12/2017 at 17:36:44
 *********************************************/
/*********************************************
 * OPL 12.6.0.0 Model
 * Author: pau
 * Creation Date: 04/11/2017 at 21:56:39
 *********************************************/

int nNurses=...;
int minHours=...;
int maxHours=...;
int maxConsec=...;
int maxPresence=...;
int hours=...;
range N=1..nNurses;
range H=1..hours;
int demand[h in H]=...;
//decision vars
dvar boolean w[n in N, h in H];
dvar boolean z[n in N];
dvar int s[n in N];
dvar int e[n in N];
// debugging vars
//int desiredZ[n in N]=...;
int centroides=...;

// minimize the number of nurses working
minimize sum(n in N) z[n];

subject to {

	//set the zn values to 1, according to nurses that work any hour during the shift
	forall(n in N){
		hours*z[n] >= sum(h in H) w[n,h];
		z[n] <= sum(h in H) w[n,h];
	}
	

	// at any hour h, at least demandh nurses should be working
	forall (h in H)
		sum(n in N) w[n,h] >= demand[h];
		
	//each nurse that works, should work at least minHours
	forall (n in N)
		sum(h in H) w[n,h] >= minHours*z[n];
	
	//each nurse that works, should work at most maxHours
	forall (n in N)
		sum(h in H) w[n,h] <= maxHours*z[n];
		
	//each nurse works at most maxConsec consecutive hours
	forall (n in N, h1 in 1..(hours-maxConsec))
		sum(h in h1..(h1+maxConsec)) w[n,h] <= maxConsec;
		
	//each nurse can stay in the hospital at most maxPresence hours
	
	//----> en is the highest hour that the nurse works.
	//----> this includes making en 0 if zn is 0
	//----> make en=0 if zn=0 (the nurse does not work) and at most hours
	forall(n in N)
		hours*z[n] >= e[n];
	forall(n in N, h in H)
		e[n] >= h*w[n,h];
		  	
	//---> sn is the minimum hour that the nurse works
	//---> this includes making sn 0 if zn is 0,
	//--->  this will not assure that s[n] is just the min, but it will be 
	//---> between 0 and the min hour
	forall(n in N)
	  s[n] >= 0 ;
	forall(n in N, h in H){
		s[n] <= (h - hours)*w[n,h] + hours*z[n];
	}

	//---> finally apply the maxPresence constraint
	forall(n in N)
		e[n] - s[n] + 1 - (2*hours)*(1 - z[n]) <= maxPresence*z[n];
		

			
	//each nurse can rest at most one consecutive hour
	forall(n in N, h in 2..(hours - 2))
	  (2*(hours + 1)) - (2*(hours + 1))*w[n,h-1] + (2*(hours + 1))*w[n,h] + (2*(hours + 1))*w[n,h+1]  >= sum(h1 in (h+1)..hours) w[n,h1];



}	