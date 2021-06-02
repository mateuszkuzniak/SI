include "globals.mzn"; 

% Dane wejściowe
int: rows;
int: columns;
int: max_steps;
array[1..rows, 1..columns] of int: board;

% Wyznaczenie największej liczby znajdującej się na planszy
int: max_value = max([board[i, j] | i in 1..rows, j in 1..columns]);

% Utworzenie tabeli jednowymiarowej wielkości max_steps elementów o wartościach z przedziału <1, rows>, która przechowuje numer wiersza każdego kroku rozwiązania
array[1..max_steps] of var 1..rows: row;

% Utworzenie tabeli jednowymiarowej wielkości max_steps elementów o wartościach z przedziału <1, columns>, która przechowuje numer kolumny każdego kroku rozwiązania
array[1..max_steps] of var 1..columns: column;

% Utworzenie tabeli jednowymiarowej wielkości max_steps elementów o wartościach z przedziału <0, max_value>, która przechowuje ilość punktów każdego kroku rozwiązania
array[1..max_steps] of var 0..max_value: points;

% Wyliczenie sumy wszystkich punktów na planszy
int: board_sum = sum([board[i, j] | i in 1..rows, j in 1..columns where board[i, j] > 0]);
% Utworzenie zmiennej o wartości znajdującej się w przedziale <0, board_sum>
var 0..board_sum: sum_points;

% Ograniczenie zapewniające, że każdy krok jest różny (żadna para kroków nie ma takich samych współrzędnych)
constraint forall(
  step in 1..max_steps, next in step+1..max_steps)(
    row[step] != row[next] \/ column[step] != column[next]
   );

% Ograniczenie ustalające ilość punktów na każdym kroku rozwiązania
constraint forall(
  step in 1..max_steps)(
    points[step] = board[row[step], column[step]]
  );
  
% Ograniczenie sumy punktów zdobytych dla danego rozwiązania
constraint
  sum_points = sum(points);
  
% Ograniczenie sprawdzające czy pole czarne nie znajduje się w rozwiązaniu
constraint forall(
  step in 1..max_steps) (
  board[row[step], column[step]] != -1
  );
 
% Ograniczenie sprawdzające, że kolejny krok jest w bezpośrednim kontakcie z obecnym (tzn. w odległości jednego pola nie wliczając przekątnych)
constraint 
  forall(step in 1..max_steps - 1)(
    abs(row[step] - row[step+1]) + abs(column[step] - column[step+1]) = 1
  );

% Ograniczenie sprawdzjące czy ostatni krok w rozwiązaniu znajduje się w bezpośrenim kontakcie z pierwszym krokiem w celu zamknięcia pętli
constraint
  abs(row[max_steps] - row[1]) + abs(column[max_steps] - column[1]) = 1;
  
  
solve maximize sum_points;


output [
"x: " ++ show(row) ++ "\n"++
"y: " ++ show(column) ++ "\n"++
"points: " ++ show(points) ++ "\n"++
"sum_points: " ++ show(sum_points) ++ "\n"
];