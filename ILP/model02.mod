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
range N=1..nNurses;
range H=1..24;
int demand[h in H]=...;
//decision vars
dvar boolean w[n in N, h in H];
dvar boolean z[n in N];
dvar int s[n in N];
dvar int e[n in N];
dvar boolean r[n in N, h in H];
dvar boolean wa[n in N, h in H];
dvar boolean wb[n in N, h in H];




// minimize the number of nurses working
minimize sum(n in N) z[n];

subject to {

	//set the zn values to 1, according to nurses that work any hour during the shift
	forall(n in N){
		24*z[n] >= sum(h in H) w[n,h];
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
	forall (n in N, h1 in 1..(24-maxConsec))
		sum(h in h1..(h1+maxConsec)) w[n,h] <= maxConsec;
		
	//each nurse can stay in the hospital at most maxPresence hours
	
	//----> en is the highest hour that the nurse works.
	//----> this includes making en 0 if zn is 0
	//----> make en=0 if zn=0 (the nurse does not work) and at most 24
	forall(n in N)
		24*z[n] >= e[n];
	forall(n in N, h in H)
		e[n] >= h*w[n,h];
		  	
	//---> sn is the minimum hour that the nurse works
	//---> this includes making sn 0 if zn is 0,
	//--->  this will not assure that s[n] is just the min, but it will be 
	//---> between 0 and the min hour
	forall(n in N)
	  s[n] >= 0 ;
	forall(n in N, h in H){
		s[n] <= (h - 24)*w[n,h] + 24*z[n];
	}

	//---> finally apply the maxPresence constraint
	forall(n in N)
		e[n] - s[n] + 1 <= maxPresence*z[n];
		

			
	//each nurse can rest at most one consecutive hour
	forall(n in N, h in 2..23){
		r[n,h] 	== 1 - w[n,h];
		wa[n,h] == w[n,h+1];
		wb[n,h] == w[n,h-1];
		2*50*(1 - r[n,h]) + 50*wb[n,h] - 50*wa[n,h] + 50*r[n,h] >= sum(h1 in 1..h) w[n,h1];
	}
	


}	