include "globals.mzn"; 

int: rows;
int: columns;
int: steps;
array[1..rows, 1..columns] of int: board;

int: max_value = max([board[i, j] | i in 1..rows, 
                                    j in 1..columns]);

array[1..steps] of var 1..rows: row;
array[1..steps] of var 1..columns: column;
array[1..steps] of var 0..max_value: points;

int: board_sum = sum([board[i, j] | i in 1..rows, 
                                    j in 1..columns 
                      where board[i, j] > 0]);

var 0..board_sum: sum_points;

constraint forall(
  step in 1..steps, next in step+1..steps)(
    row[step] != row[next] \/ 
    column[step] != column[next]
   );

constraint forall(
  step in 1..steps)(
    points[step] = board[row[step], column[step]]
  );
  
constraint
  sum_points = sum(points);
  
constraint forall(
  step in 1..steps) (
  board[row[step], column[step]] != -1
  );
 
constraint 
  forall(step in 1..steps - 1)(
    abs(row[step] - row[step+1]) + 
    abs(column[step] - column[step+1]) = 1
  );

constraint
  abs(row[steps] - row[1]) + 
  abs(column[steps] - column[1]) = 1;
  
solve maximize sum_points;