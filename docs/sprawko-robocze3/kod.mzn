int: x = 10;
set of int: RANGE = 1..x;
set of int: RANGE1 = 0..x;
set of int: RANGE2 = 2..x - 1;
array[RANGE, RANGE] of var RANGE1: plansza;
/* 
0 - ściana
1 - ścieżka
*/

constraint plansza[1,1] = 6;
constraint plansza[7,1] = 2;
constraint plansza[5,5] = 4;
constraint plansza[10,3] = 7;
constraint plansza[10,1] = 1;

int: n=0;
int: m=0;

/*ograniczenia dla pól z liczbą większą niż 1 określające widzenie z tego pola n pól gdzie n to liczba danego pola*/
constraint forall(i in RANGE, j in RANGE, n = plansza[i,j], m = plansza[i,j])(
  if plansza[i,j] > 1 then 
    forall(k in 1..n - 1 where m > 0)(
      plansza[i,j + k] = 1
    )
  endif);



/*ograniczenia związane z posiadaniem sąsiada*/

/*środek planszy*/
constraint forall(i in RANGE2, j in RANGE2) (
  if plansza[i, j] > 0 then
    count(k in plansza[i - 1, j - 1..j + 1])(k>0) + count(k in plansza[i, j - 1..j + 1])(k>0) + count(k in plansza[i + 1, j - 1..j + 1])(k>0) > 1
  endif
  );

/*górna krawędź planszy bez narożników*/
constraint forall(i = 1, j in RANGE2) (
  if plansza[i, j] > 0 then
    count(k in plansza[i, j - 1..j + 1])(k>0) + count(k in plansza[i + 1, j - 1..j + 1])(k>0) > 1
  endif
  );

/*dolna krawędź planszy bez narożników*/
constraint forall(i = 10, j in RANGE2) (
  if plansza[i, j] > 0 then
    count(k in plansza[i, j - 1..j + 1])(k>0) + count(k in plansza[i - 1, j - 1..j + 1])(k>0) > 1
  endif
  );

/*lewa krawędź planszy bez narożników*/
constraint forall(i in RANGE2, j = 1) (
  if plansza[i, j] > 0 then
    count(k in plansza[i - 1, j..j + 1])(k>0) + count(k in plansza[i, j..j + 1])(k>0) + count(k in plansza[i + 1, j..j + 1])(k>0) > 1
  endif
  );

/*prawa krawędź planszy bez narożników*/
constraint forall(i in RANGE2, j = 10) (
  if plansza[i, j] > 0 then
    count(k in plansza[i - 1, j - 1..j])(k>0) + count(k in plansza[i, j - 1..j])(k>0) + count(k in plansza[i + 1,j - 1..j])(k>0) > 1
  endif
  );

/*lewy-górny narożnik planszy*/
constraint forall(i = 1, j = 1) (
  if plansza[i, j] > 0 then
    count(k in plansza[i, j..j + 1])(k>0) + count(k in plansza[i + 1, j..j + 1])(k>0) > 1
  endif
  );

/*prawy-górny narożnik planszy*/
constraint forall(i = 1, j = 10) (
  if plansza[i, j] > 0 then
    count(k in plansza[i, j - 1..j])(k>0) + count(k in plansza[i + 1, j - 1..j])(k>0) > 1
  endif
  );

/*lewy-dolny narożnik planszy*/
constraint forall(i = 10, j = 1) (
  if plansza[i, j] > 0 then
    count(k in plansza[i, j..j + 1])(k>0) + count(k in plansza[i - 1, j..j + 1])(k>0) > 1
  endif
  );

/*prawy-dolny narożnik planszy*/
constraint forall(i = 10, j = 10) (
  if plansza[i, j] > 0 then
    count(k in plansza[i, j - 1..j])(k>0) + count(k in plansza[i - 1, j - 1..j])(k>0) > 1
  endif
  );

output [show([plansza[i,j]| j in RANGE]) ++ "\n"| i in RANGE];

solve satisfy;