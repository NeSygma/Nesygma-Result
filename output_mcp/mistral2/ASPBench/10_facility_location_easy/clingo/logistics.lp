% --- Declare customers and their coordinates ---
customer(1). coordinates(1, 1, 1).
customer(2). coordinates(2, 2, 4).
customer(3). coordinates(3, 4, 2).
customer(4). coordinates(4, 5, 5).
customer(5). coordinates(5, 7, 1).
customer(6). coordinates(6, 8, 3).
customer(7). coordinates(7, 3, 6).
customer(8). coordinates(8, 6, 4).

% --- Declare facilities and their coordinates and opening costs ---
facility(a). coordinates(a, 2, 2). opening_cost(a, 100).
facility(b). coordinates(b, 4, 4). opening_cost(b, 120).
facility(c). coordinates(c, 6, 2). opening_cost(c, 110).
facility(d). coordinates(d, 3, 5). opening_cost(d, 90).
facility(e). coordinates(e, 7, 3). opening_cost(e, 130).

% --- Calculate Manhattan distance between customer C and facility F ---
distance(C, F, D) :-
    customer(C),
    facility(F),
    coordinates(C, X1, Y1),
    coordinates(F, X2, Y2),
    D = (X1 - X2) + (Y1 - Y2).

distance(C, F, D) :-
    customer(C),
    facility(F),
    coordinates(C, X1, Y1),
    coordinates(F, X2, Y2),
    D = (X2 - X1) + (Y1 - Y2).

distance(C, F, D) :-
    customer(C),
    facility(F),
    coordinates(C, X1, Y1),
    coordinates(F, X2, Y2),
    D = (X1 - X2) + (Y2 - Y1).

distance(C, F, D) :-
    customer(C),
    facility(F),
    coordinates(C, X1, Y1),
    coordinates(F, X2, Y2),
    D = (X2 - X1) + (Y2 - Y1).

% --- Service cost = distance * 5 ---
service_cost(C, F, Cost) :-
    distance(C, F, D),
    Cost = D * 5.

% --- Choice rule: decide which facilities are opened ---
{ opened(F) : facility(F) }.

% --- Assign customers to facilities, respecting constraints ---
% A facility can serve a customer only if:
% 1. The distance <= 3
% 2. The facility is opened
serves(F, C) :-
    opened(F),
    distance(C, F, D),
    D <= 3,
    customer(C),
    facility(F).

% --- Each customer must be served by at least one facility ---
:- customer(C), not serves(_, C).

% --- Calculate total opening cost ---
total_opening_cost(Total) :-
    Total = #sum { Cost : opened(F), opening_cost(F, Cost) }.

% --- Calculate total service cost ---
total_service_cost(Total) :-
    Total = #sum { Cost : serves(F, C), service_cost(C, F, Cost) }.

% --- Total cost = opening cost + service cost ---
total_cost(Total) :-
    total_opening_cost(OpeningCost),
    total_service_cost(ServiceCost),
    Total = OpeningCost + ServiceCost.

% --- Minimize total cost ---
#minimize { Total : total_cost(Total) }.

% --- Show the required output ---
#show opened/1.
#show serves/2.
#show total_cost/1.