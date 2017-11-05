AMMM Project
=============


1. Modelling
---------


### Decision vars


- $ w_{n,h} (\mathbb{B})  : \text{ whether the nurse n works at the hour h }  $
- $ z_{n} (\mathbb{B})  : \text{ whether the nurse n works during the shift(24h) or not } $
 	- $ z{n} = 1  \Rightarrow \text{ The nurse n works at least 1 hour, } \exists h, w_{n,h} = 1 $
 	- $ z{n} = 0 \Rightarrow \forall h, w_{n,h} = 0 $
- $  s_{n} (\mathbb{N}) : \text{hour in which the nurse n starts working, thus having $ w_{n,s_{n}}=1 $ and  $ w_{n,s_{n}-1}=0 $ (if $ s_{n} > 0 $ )} $
- $  e_{n} (\mathbb{N}) : \text{hour in which the nurse n stops working, thus having $ w_{n,e_{n}}=1 $ and  $ w_{n,e_{n}+i}=0,\forall i : e_{n} < i \leq 24 $ (if $ e_{n} < 24 $ )} $


### Known instance variables

* $ demand_h $
* nNurses
* minHours
* maxHours
* maxConsec
* maxPresence


### Objective function

Min: $ \sum\limits_{n=1}^{nNurses} z_{n}  $

### Constraints

* set the zn values correctly:
$  \forall n: 1 \leq n \leq nNurses,  \\\
	24 \cdot z_{n}  \geq \sum\limits_{1 \leq h \leq 24} w_{n,h} \\\
   z_{n} \leq \sum\limits_{1 \leq h \leq 24} w_{n,h}
$

* At any hour h, at least demandh nurses should be working:
$ \forall h : 1 \leq h \leq 24, \\\
 \sum\limits_{1 \leq n \leq nNurses} w_{n,h} \geq demand_{h}
$

* Each nurse that works, should work at least minHours:
$ \forall n: 1 \leq n \leq nNurses \\\
	\sum\limits_{1 \leq h \leq 24} w_{n,h} \geq minHours \cdot z_{n}
$

* Each nurse that works, should work at most maxHours:
$ \forall n: 1 \leq n \leq nNurses \\\
	\sum\limits_{1 \leq h \leq 24} w_{n,h} \leq maxHours \cdot z_{n}
$

* Each nurse works at most maxConsec consecutive hours: 
$	\forall n:  1 \leq n \leq nNurses, \\\
	\forall h_{1}:  1 \leq h_{1} \leq 24 - maxConsec, \\\
	\sum\limits_{ h_{1} \leq h \leq h_{1} + maxConsec} w_{n,h} \leq maxConsec $

* Each nurse can stay in the hospital at most maxPresence hours:

$  \forall n:  1 \leq n \leq nNurses, \forall h: 1 \leq h \leq 24, e_{n} \geq h \cdot w_{n,h} \\\ 
 \forall n:  1 \leq n \leq nNurses, \forall h: 1 \leq h \leq 24, s_{n} \leq (h - 24) \cdot w_{n,h} + 24 \\\
  \forall n:  1 \leq n \leq nNurses, e_{n} - s_{n} + 1 \leq maxPresence $

* Each nurse can rest at most one consecutive hour:
	- this idea is not linear : $  \forall n:  1 \leq n \leq nNurses \\\
		\forall h_{1}: s_{n} \leq h_{1} \leq e_{n} - 1  \\\ 
		\sum\limits_{h_{1} \leq h \leq h_{1} + 1} w_{n,h} \geq 1 $

	- this is still under evaluation: $ \forall n:  1 \leq n \leq nNurses, \forall h: 1 \leq h \leq 24, f_{n,h} = \sum\limits_{h \leq h_{1} \leq 24 } w_{n,h_{1}}   \\\
	\forall n:  1 \leq n \leq nNurses, \forall h: 2 \leq h \leq 24, a_{n,h} = w_{n,h-1} - w_{n,h}  \\\
	 \forall n:  1 \leq n \leq nNurses, \forall h: 1 \leq h \leq 22, b_{n,h} = f_{n,h} - f_{n,h+2}  \\\
	 \forall n:  1 \leq n \leq nNurses, \forall h: 2 \leq h \leq 22, c_{n,h} = a_{n,h} + 25 \cdot(1 - a_{n,h}) + 25 \cdot b_{n,h}  \\\
	 \forall n:  1 \leq n \leq nNurses, \forall h: 1 \leq h \leq 22, d_{n,h} = f_{n,h+1} \\\
	 \forall n:  1 \leq n \leq nNurses, \forall h: 2 \leq h \leq 22, c_{n,h} >= d_{n,h}  \\\
	 $

	  - an example scenario

$$
\begin{array}{|c|cccccccccccccccccc|}
\hline
\text{wnh}               & 0 & 0 & 0 & 1 & 1 & 1 & 0 & 1 & 1 & 1 & 0 & 0 & 1 & 1 & 1 & 0 & 0 & 0 \\\
\hline
\text{f(h)=wnh+..+wn(24)} 
						 & 9 & 9 & 9 & 9 & 8 & 7 & 6 & 6 & 5 & 4 & 3 & 3 & 3 & 2 & 1 & 0 & 0 & 0 \\\
\text{a(h)=wn(h-1)-wnh}  &   & 0 & 0 &-1 & 0 & 0 & 1 &-1 & 0 & 0 & 1 & 0 &-1 & 0 & 0 & 1 & 0 & 0 \\\
\text{b(h)=f(h)-f(h+2)}  & 0 & 0 & 1 & 2 & 2 & 1 & 1 & 2 & 2 & 1 & 0 & 1 & 2 & 2 & 1 & 0 &   &  \\\
\text{c(h)=a+(1-a)25+b25}     &   & 25 & 50 & 99 & 75 & 50 & 26 & 99 & 75 & 50 & 1 & 50 & 99 & 75 & 50 & 1 &   & \\\
\text{d(h)=f(h+1)} 
						 & 9 & 9 & 9 & 8 & 7 & 6 & 6 & 5 & 4 & 3 & 3 & 3 & 2 & 1 & 0 & 0 &  &  \\\
\text{c(h)>=d(h)}        &   & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 0 & 1 & 1 & 1 & 1 & 1 &  \\\
\hline
\end{array}
$$






