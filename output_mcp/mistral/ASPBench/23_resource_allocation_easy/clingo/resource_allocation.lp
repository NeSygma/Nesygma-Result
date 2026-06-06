% Define resources and their capacities
resource(a, 100).
resource(b, 80).
resource(c, 60).

% Task data: task(Id, Value, ResourceA, ResourceB, ResourceC)
task(0, 50, 30, 20, 10).
task(1, 40, 25, 15, 15).
task(2, 60, 20, 30, 20).
task(3, 35, 15, 25, 10).
task(4, 70, 40, 10, 25).
task(5, 45, 20, 20, 15).

% Choice: select a task or not
{ selected(T) : task(T, _, _, _, _) }.

% Calculate total value
total_value(V) :- V = #sum { Val, T : task(T, Val, _, _, _), selected(T) }.

% Calculate resource usage for each resource type
resource_used(a, U) :- U = #sum { A, T : task(T, _, A, _, _), selected(T) }.
resource_used(b, U) :- U = #sum { B, T : task(T, _, _, B, _), selected(T) }.
resource_used(c, U) :- U = #sum { C, T : task(T, _, _, _, C), selected(T) }.

% Constraints: resource usage <= capacity
:- resource(a, CapA), resource_used(a, Ua), Ua > CapA.
:- resource(b, CapB), resource_used(b, Ub), Ub > CapB.
:- resource(c, CapC), resource_used(c, Uc), Uc > CapC.

% Optimization
#maximize { V : total_value(V) }.

% Show the selected tasks and total value
#show selected/1.
#show total_value/1.