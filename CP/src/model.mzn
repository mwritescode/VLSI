include "globals.mzn";

int: num_circuits;
int: width;

array[1..num_circuits] of int: circuits_w;
array[1..num_circuits] of int: circuits_h;


int: area_min = sum([circuits_h[i] * circuits_w[i] | i in 1..num_circuits]);
var 0..area_min: white_space = width*height - area_min;
int: min_height = max(max(circuits_h), floor(area_min/width));

var min_height..sum(circuits_h): height;
array[1..num_circuits] of var 0..width: circuits_x;
array[1..num_circuits] of var 0..sum(circuits_h): circuits_y;

%array[1..num_circuits] of int: order = reverse(arg_sort([max(circuits_h[i], circuits_w[i]) | i in 1..num_circuits]));
%array[1..num_circuits] of int: order = reverse(arg_sort([circuits_h[i] | i in 1..num_circuits]));
array[1..num_circuits] of int: order = reverse(arg_sort([circuits_w[i] | i in 1..num_circuits]));
%array[1..num_circuits] of int: order = reverse(arg_sort([circuits_w[i] * circuits_h[i] | i in 1..num_circuits]));

array[1..width] of var 0..1: first_row;

% Always set the rectangles so that there are no blank spaces in the bottom row of the board
% Basically breaks symmetries related to blank spaces
constraint forall(i in 0..width-1)(
  first_row[i+1] = 1 <-> card({j | j in 1..num_circuits where circuits_x[j] <= i /\ circuits_x[j] + circuits_w[j] > i /\ circuits_y[j] == 0}) >= 1);
constraint all_equal(first_row) /\ first_row[1] == 1;

constraint cumulative(circuits_x, circuits_w, circuits_h, height);
constraint cumulative(circuits_y, circuits_h, circuits_w, width);

constraint diffn(circuits_x, circuits_y, circuits_w, circuits_h);
constraint forall(i in 1..num_circuits) (circuits_x[i] + circuits_w[i] <= width /\ circuits_y[i] + circuits_h[i] <= height);

% Implied constraints suggested by prof. (point 2)
constraint implied_constraint(forall(i in 0..width)(sum([circuits_h[j] | j in 1..num_circuits where circuits_x[j] <= i /\ (circuits_x[j] + circuits_w[j]) > i]) <= height));
constraint implied_constraint(forall(i in 0..height)(sum([circuits_w[j] | j in 1..num_circuits where circuits_y[j] <= i /\ (circuits_y[j] + circuits_h[j]) > i]) <= width));

constraint symmetry_breaking_constraint(circuits_x[order[1]] = 0 /\ circuits_y[order[1]] = 0);

constraint symmetry_breaking_constraint(
forall(i, j in order) (
  if i>j then
    (if circuits_x[i] == circuits_x[j] then
        if circuits_w[i] == circuits_w[j] then
       % breaks swapping of same-width and same-x blocks
           circuits_y[i] < circuits_y[j] 
         elseif circuits_h[i] == circuits_h[j] then
         % makes it so a block placed on x=5,y=0 and high 4 and another block placed on, say, x=5,y=9 and high 4
         % cannot be swapped
           circuits_y[i] < circuits_y[j] 
         else true endif
     endif)
  endif)
);


solve :: seq_search([int_search([circuits_x[i] | i in order], input_order, indomain_min, complete), int_search([circuits_y[i] | i in order], input_order, indomain_min, complete)]) minimize area_min*height+white_space;

output ["\(width) \(height)\n" ++ "\(num_circuits)\n" ++ concat([
    "\(circuits_w[j]) \(circuits_h[j]) \(circuits_x[j]) \(circuits_y[j])\n" | j in 1..num_circuits])];

