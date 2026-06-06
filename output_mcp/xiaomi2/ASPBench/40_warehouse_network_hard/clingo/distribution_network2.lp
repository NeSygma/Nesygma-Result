% ==========================================
% Distribution Network Design - ASP Model (Optimized)
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

% --- Connectivity ---
can_supply(h1, r1). can_supply(h1, r2). can_supply(h2, r3). can_supply(h2, r4).
can_serve(r1, c1). can_serve(r1, c2). can_serve(r2, c2). can_serve(r2, c3).
can_serve(r3, c4). can_serve(r3, c5). can_serve(r4, c5). can_serve(r4, c6).

% --- Maintenance ---
maint_r(r2, 2). maint_h(h1, 4).

% ==========================================
% Precompute valid (R, C, T) triples
% ==========================================
valid_serve(R, C, T) :- can_serve(R, C), time(T), tw(C, T1, T2), T >= T1, T <= T2, not maint_r(R, T).

% ==========================================
% Decision Variables
% ==========================================
{ open_hub(H) } :- hub(H).
{ open_regional(R) } :- regional(R).
{ supply(H, R) : hub(H), can_supply(H, R) } 1 :- open_regional(R).
{ serve(R, C, T) : valid_serve(R, C, T) } 1 :- customer(C).

% ==========================================
% Constraints
% ==========================================

% Must be open
:- serve(R, C, T), not open_regional(R).
:- supply(H, R), not open_hub(H).

% Hub maintenance
:- serve(R, C, T), supply(H, R), maint_h(H, T).

% Regional capacity
regional_demand(R, Dem) :- serve(R, C, T), demand(C, Dem), regional(R).
:- regional(R), regional_cap(R, Cap), #sum { Dem, C, T : serve(R, C, T), demand(C, Dem) } > Cap.

% Hub capacity
:- hub(H), hub_cap(H, Cap), #sum { Dem, R, C, T : supply(H, R), serve(R, C, T), demand(C, Dem) } > Cap.

% Truck limits
:- hub(H), time(T), trucks(H, K), #count { C, R : supply(H, R), serve(R, C, T) } > K.

% ==========================================
% Objective: Minimize Total Cost
% ==========================================

% Fixed opening costs
:~ open_hub(H), hub_cost(H, Cost). [Cost@1]
:~ open_regional(R), regional_cost(R, Cost). [Cost@1]

% Hub-to-Regional transport: unit_cost * total_demand_through_regional
% We need total demand per regional. Use a helper.
reg_total_dem(R, TD) :- TD = #sum { Dem, C, T : serve(R, C, T), demand(C, Dem) }, regional(R).
:~ supply(H, R), hr_cost(H, R, UC), reg_total_dem(R, Dem), Cost = UC * Dem. [Cost@1]

% Regional-to-Customer transport: unit_cost * customer_demand
:~ serve(R, C, T), rc_cost(R, C, UC), demand(C, Dem), Cost = UC * Dem. [Cost@1]

% ==========================================
% Output
% ==========================================
#show open_hub/1.
#show open_regional/1.
#show supply/2.
#show serve/3.