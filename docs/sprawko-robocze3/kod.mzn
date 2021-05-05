int: x = 10;
set of int: RANGE = 1..x;
set of int: RANGE1 = 0..x;
array[RANGE, RANGE] of var RANGE1: plansza;
/* 
0 - ściana
1 - ścieżka
*/

constraint plansza[1,1] = 6;
constraint plansza[6,2] = 4;

int: n=0;
int: m=0;
include "alldifferent.mzn";
constraint forall(i in RANGE,j in RANGE,  n = plansza[i,j], m = plansza[i,j])(
  if plansza[i,j] > 1 then 
    forall(k in 2..n where m > 0)(
      plansza[i,k] = 1
    )/\
    forall(l in 2..n where m > 0)(
      plansza[l,j] = 1
    )
  endif);


output [show([plansza[i,j]| j in RANGE]) ++ "\n"| i in RANGE];

solve satisfy;