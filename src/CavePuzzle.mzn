%Plansza wejścia
set of int: FIELD_SIZE = 1..9;
set of int: ALL_OPTS = 0..9;

%Plansza problemu
set of int: FIELD_OPT = 1..9;
array[FIELD_SIZE, FIELD_SIZE] of var FIELD_OPT: puzzle;

%Definicja mniejszych kwadratów
array[FIELD_SIZE] of FIELD_SIZE: square_start_x = [((k-1) div 3)*3 + 1| k in FIELD_SIZE];
array[FIELD_SIZE] of FIELD_SIZE: square_start_y = [((k-1) mod 3)*3 + 1| k in FIELD_SIZE];


%Ograniczenie - unikalność w rzędzie, kolumnie i kwadracie
include "alldifferent.mzn";
constraint forall(row       in FIELD_SIZE)(alldifferent([puzzle[row, col] | col in FIELD_SIZE])); 
constraint forall(col       in FIELD_SIZE)(alldifferent([puzzle[row, col] | row in FIELD_SIZE])); 
constraint forall(square_ix in FIELD_SIZE)(alldifferent([puzzle[row, col] | row in square_start_x[square_ix]..square_start_x[square_ix]+2, 
                                                                            col in square_start_y[square_ix]..square_start_y[square_ix]+2]));
%Dane w 'data.dzn'
array[FIELD_SIZE, FIELD_SIZE] of ALL_OPTS: puzzle_input;
  
%Ograniczenie - (dla każdego niepustego pola wejścia)(przepisz wejście do planszy problemu)
constraint forall(row, col in FIELD_SIZE where puzzle_input[row, col] > 0)(puzzle[row, col] = puzzle_input[row, col]);

%Format wyjścia
output [show([puzzle[row, col] | col in FIELD_SIZE]) ++ "\n" | row in FIELD_SIZE];

solve satisfy;