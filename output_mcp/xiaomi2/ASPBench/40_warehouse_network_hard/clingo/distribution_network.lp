% ==========================================
% Distribution Network Design - ASP Model
% ==========================================

% --- Domains ---
hub(h1). hub(h2).
regional(r1). regional(r2). regional(r3). regional(r4).
customer(c1). customer(c2). customer(c3). customer(c4). customer(c5). customer(c6).
time(1). time(2). time(3). time(4).

% --- Opening Costs ---
hub_cost(h1, 1000). hub_cost(h2, 1200).
regional_cost(r1, 200). regional_cost(r2, 250). regional_cost(r3, 220). regional_cost(r4, 180).

% --- Capacities ---
hub_cap(h1, 400). hub_cap(h2, 350).
regional_cap(r1, 70). regional_cap(r2, 80). regional_cap(r3, 60). regional_cap(r4, 90).

% --- Trucks per hub per time slot ---
trucks(h1, 2). trucks(h2, 1).

% --- Customer Demands ---
demand(c1, 20). demand(c2, 30). demand(c3, 15). demand(c4, 25). demand(c5, 35). demand(c6, 10).

% --- Time Windows ---
tw(c1, 2, 3). tw(c2, 1, 2). tw(c3, 3, 4). tw(c4, 1, 4). tw(c5, 2, 4). tw(c6, 1, 1).

% --- Hub-to-Regional Transport Costs (per unit) ---
hr_cost(h1, r1, 5). hr_cost(h1, r2, 6). hr_cost(h2, r3, 5). hr_cost(h2, r4, 6).

% --- Regional-to-Customer Transport Costs (per unit) ---
rc_cost(r1, c1, 10). rc_cost(r1, c2, 12). rc_cost(r2, c2, 13). rc_cost(r2, c3, 15).
rc_cost(r3, c4, 9). rc_cost(r3, c5, 11). rc_cost(r4, c5, 14). rc_cost(r4, c6, 7).

% --- Connectivity: Hub can supply Regional ---
can_supply(h1, r1). can_supply(h1, r2). can_supply(h2, r3). can_supply(h2, r4).

% --- Connectivity: Regional can serve Customer ---
can_serve(r1, c1). can_serve(r1, c2). can_serve(r2, c2). can_serve(r2, c3).
can_serve(r3, c4). can_serve(r3, c5). can_serve(r4, c5). can_serve(r4, c6).

% --- Maintenance Schedules ---
maintenance_regional(r2, 2).
maintenance_hub(h1, 4).

% ==========================================
% Precompute valid (R, C, T) triples
% ==========================================
valid_serve(R, C, T) :- can_serve(R, C), time(T), tw(C, T1, T2), T >= T1, T <= T2, not maintenance_regional(R, T).

% ==========================================
% Decision Variables (Choice Rules)
% ==========================================

% Choose which hubs to open
{ open_hub(H) } :- hub(H).

% Choose which regionals to open
{ open_regional(R) } :- regional(R).

% Choose which hub supplies each open regional (exactly one)
{ supply(H, R) : hub(H), can_supply(H, R) } 1 :- open_regional(R).

% Choose which regional serves each customer at which time (exactly one)
{ serve(R, C, T) : valid_serve(R, C, T) } 1 :- customer(C).

% ==========================================
% Constraints
% ==========================================

% Constraint 1: Customer can only be served by an open regional
:- serve(R, C, T), not open_regional(R).

% Constraint 1b: Open regional must be supplied by an open hub
:- supply(H, R), not open_hub(H).

% Constraint 6: No deliveries through hub during its maintenance
:- serve(R, C, T), supply(H, R), maintenance_hub(H, T).

% Constraint 7: Regional capacity
total_demand_regional(R, D) :- D = #sum { Dem, C, T : serve(R, C, T), demand(C, Dem) }, regional(R).
:- total_demand_regional(R, D), regional_cap(R, Cap), D > Cap.

% Constraint 8: Hub capacity
total_demand_hub(H, D) :- D = #sum { Dem, R, C, T : supply(H, R), serve(R, C, T), demand(C, Dem) }, hub(H).
:- total_demand_hub(H, D), hub_cap(H, Cap), D > Cap.

% Constraint 9: Truck limits per hub per time slot
delivery_count(H, T, N) :- N = #count { C, R : supply(H, R), serve(R, C, T) }, hub(H), time(T).
:- delivery_count(H, T, N), trucks(H, K), N > K.

% ==========================================
% Objective: Minimize Total Cost
% ==========================================

% Fixed opening costs
hub_fixed_cost(C) :- C = #sum { Cost, H : open_hub(H), hub_cost(H, Cost) }.
regional_fixed_cost(C) :- C = #sum { Cost, R : open_regional(R), regional_cost(R, Cost) }.
total_fixed_cost(FC) :- hub_fixed_cost(HC), regional_fixed_cost(RC), FC = HC + RC.

% Hub-to-Regional transport costs (unit cost * total demand through regional)
hr_link_cost(H, R, Cost) :- supply(H, R), hr_cost(H, R, UnitCost), total_demand_regional(R, Dem), Cost = UnitCost * Dem.
total_hr_cost(C) :- C = #sum { Cost, H, R : hr_link_cost(H, R, Cost) }.

% Regional-to-Customer transport costs (unit cost * customer demand)
rc_link_cost(R, Cust, Cost) :- serve(R, Cust, T), rc_cost(R, Cust, UnitCost), demand(Cust, Dem), Cost = UnitCost * Dem.
total_rc_cost(C) :- C = #sum { Cost, R, Cust : rc_link_cost(R, Cust, Cost) }.

% Total cost
total_cost(TC) :- total_fixed_cost(FC), total_hr_cost(HRC), total_rc_cost(RCC), TC = FC + HRC + RCC.

% Minimize total cost
#minimize { TC : total_cost(TC) }.

% ==========================================
% Output
% ==========================================
#show open_hub/1.
#show open_regional/1.
#show supply/2.
#show serve/3.
#show total_cost/1.