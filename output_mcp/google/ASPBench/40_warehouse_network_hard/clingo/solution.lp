% --- Data ---
hub(h1; h2).
regional(r1; r2; r3; r4).
customer(c1; c2; c3; c4; c5; c6).
time(1..4).

opening_cost_hub(h1, 1000).
opening_cost_hub(h2, 1200).
opening_cost_regional(r1, 200).
opening_cost_regional(r2, 250).
opening_cost_regional(r3, 220).
opening_cost_regional(r4, 180).

capacity_hub(h1, 400).
capacity_hub(h2, 350).
capacity_regional(r1, 70).
capacity_regional(r2, 80).
capacity_regional(r3, 60).
capacity_regional(r4, 90).

trucks_hub(h1, 2).
trucks_hub(h2, 1).

demand(c1, 20).
demand(c2, 30).
demand(c3, 15).
demand(c4, 25).
demand(c5, 35).
demand(c6, 10).

time_window(c1, 2, 3).
time_window(c2, 1, 2).
time_window(c3, 3, 4).
time_window(c4, 1, 4).
time_window(c5, 2, 4).
time_window(c6, 1, 1).

transport_cost_hr(h1, r1, 5).
transport_cost_hr(h1, r2, 6).
transport_cost_hr(h2, r3, 5).
transport_cost_hr(h2, r4, 6).

transport_cost_rc(r1, c1, 10).
transport_cost_rc(r1, c2, 12).
transport_cost_rc(r2, c2, 13).
transport_cost_rc(r2, c3, 15).
transport_cost_rc(r3, c4, 9).
transport_cost_rc(r3, c5, 11).
transport_cost_rc(r4, c5, 14).
transport_cost_rc(r4, c6, 7).

connect_hr(h1, r1).
connect_hr(h1, r2).
connect_hr(h2, r3).
connect_hr(h2, r4).

connect_rc(r1, c1).
connect_rc(r1, c2).
connect_rc(r2, c2).
connect_rc(r2, c3).
connect_rc(r3, c4).
connect_rc(r3, c5).
connect_rc(r4, c5).
connect_rc(r4, c6).

maintenance_r(r2, 2).
maintenance_h(h1, 4).

% --- Logic ---
{ open_hub(H) } :- hub(H).
{ open_regional(R) } :- regional(R).

% Supply uniqueness
1 { assign_hr(H, R) : connect_hr(H, R), open_hub(H) } 1 :- open_regional(R).

% Assignment uniqueness
1 { assign_rc(R, C, T) : connect_rc(R, C), time(T) } 1 :- customer(C).

% Constraints
:- assign_rc(R, C, T), not open_regional(R).
:- assign_rc(R, C, T), not assign_hr(_, R).
:- assign_rc(R, C, T), time_window(C, Start, End), T < Start.
:- assign_rc(R, C, T), time_window(C, Start, End), T > End.
:- assign_rc(R, C, T), maintenance_r(R, T).
:- assign_rc(R, C, T), assign_hr(H, R), maintenance_h(H, T).

% Regional capacity
:- regional(R), #sum { D, C : assign_rc(R, C, _), demand(C, D) } > Cap, capacity_regional(R, Cap).

% Hub capacity
:- hub(H), #sum { D, C : assign_rc(R, C, _), assign_hr(H, R), demand(C, D) } > Cap, capacity_hub(H, Cap).

% Truck limits
:- hub(H), time(T), #count { C : assign_rc(R, C, T), assign_hr(H, R) } > Trucks, trucks_hub(H, Trucks).

% Costs
% Use a helper to ensure we only count costs for opened facilities
cost_h(C) :- C = #sum { Cost, H : open_hub(H), opening_cost_hub(H, Cost) }.
cost_r(C) :- C = #sum { Cost, R : open_regional(R), opening_cost_regional(R, Cost) }.
cost_hr(C) :- C = #sum { D*Cost, H, R : assign_hr(H, R), D = #sum { D2, C2 : assign_rc(R, C2, _), demand(C2, D2) }, transport_cost_hr(H, R, Cost) }.
cost_rc(C) :- C = #sum { D*Cost, R, Cust : assign_rc(R, Cust, _), demand(Cust, D), transport_cost_rc(R, Cust, Cost) }.
total_cost(C) :- cost_h(C1), cost_r(C2), cost_hr(C3), cost_rc(C4), C = C1 + C2 + C3 + C4.

#minimize { C : total_cost(C) }.

#show open_hub/1.
#show open_regional/1.
#show assign_hr/2.
#show assign_rc/3.
#show total_cost/1.