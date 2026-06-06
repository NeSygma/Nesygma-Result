% Distribution Network Optimization Problem

% ==================== DOMAIN DECLARATIONS ====================
% Facilities
hub(h1). hub(h2).
regional(r1). regional(r2). regional(r3). regional(r4).
customer(c1). customer(c2). customer(c3). customer(c4). customer(c5). customer(c6).

% Time slots
time(1). time(2). time(3). time(4).

% ==================== FACTS ====================
% Opening costs
opening_cost(h1, 1000). opening_cost(h2, 1200).
opening_cost(r1, 200). opening_cost(r2, 250). opening_cost(r3, 220). opening_cost(r4, 180).

% Capacities
hub_capacity(h1, 400). hub_capacity(h2, 350).
regional_capacity(r1, 70). regional_capacity(r2, 80). regional_capacity(r3, 60). regional_capacity(r4, 90).

% Truck resources per hub per time slot
truck_limit(h1, 1, 2). truck_limit(h1, 2, 2). truck_limit(h1, 3, 2). truck_limit(h1, 4, 2).
truck_limit(h2, 1, 1). truck_limit(h2, 2, 1). truck_limit(h2, 3, 1). truck_limit(h2, 4, 1).

% Customer demands and time windows
demand(c1, 20). time_window(c1, 2, 3).
demand(c2, 30). time_window(c2, 1, 2).
demand(c3, 15). time_window(c3, 3, 4).
demand(c4, 25). time_window(c4, 1, 4).
demand(c5, 35). time_window(c5, 2, 4).
demand(c6, 10). time_window(c6, 1, 1).

% Transportation costs (per unit)
% Hub to Regional
transport_cost(h1, r1, 5). transport_cost(h1, r2, 6).
transport_cost(h2, r3, 5). transport_cost(h2, r4, 6).

% Regional to Customer
transport_cost(r1, c1, 10). transport_cost(r1, c2, 12).
transport_cost(r2, c2, 13). transport_cost(r2, c3, 15).
transport_cost(r3, c4, 9). transport_cost(r3, c5, 11).
transport_cost(r4, c5, 14). transport_cost(r4, c6, 7).

% Connectivity constraints
can_supply(h1, r1). can_supply(h1, r2).
can_supply(h2, r3). can_supply(h2, r4).

can_serve(r1, c1). can_serve(r1, c2).
can_serve(r2, c2). can_serve(r2, c3).
can_serve(r3, c4). can_serve(r3, c5).
can_serve(r4, c5). can_serve(r4, c6).

% Maintenance schedules
maintenance(r2, 2). maintenance(h1, 4).

% ==================== DECISION VARIABLES ====================
% Opening decisions (choice rules)
{ open_hub(H) } :- hub(H).
{ open_regional(R) } :- regional(R).

% Hub supply assignments (each open regional must be supplied by exactly one hub)
{ hub_supply(R, H) : hub(H) } 1 :- open_regional(R).

% Customer deliveries (each customer must be assigned to exactly one regional at exactly one time)
{ customer_delivery(C, R, T) : regional(R), time(T) } 1 :- customer(C).

% ==================== CONSTRAINTS ====================
% 1. Opening prerequisite: Customer can only be served by open regional, which must be supplied by open hub
:- customer_delivery(C, R, T), not open_regional(R).
:- customer_delivery(C, R, T), hub_supply(R, H), not open_hub(H).

% 2. Assignment uniqueness: Each customer assigned to exactly one regional at exactly one time
% (Already enforced by choice rule with cardinality 1)

% 3. Supply uniqueness: Each open regional supplied by exactly one hub
% (Already enforced by choice rule with cardinality 1)

% 4. Connectivity: Hub-to-Regional and Regional-to-Customer assignments must respect connectivity
:- hub_supply(R, H), not can_supply(H, R).
:- customer_delivery(C, R, T), not can_serve(R, C).

% 5. Time windows: Customer deliveries must occur within their specified time windows
:- customer_delivery(C, R, T), time_window(C, T_start, T_end), T < T_start.
:- customer_delivery(C, R, T), time_window(C, T_start, T_end), T > T_end.

% 6. Maintenance: No deliveries can pass through facilities during their maintenance time slots
:- customer_delivery(C, R, T), maintenance(R, T).
:- customer_delivery(C, R, T), hub_supply(R, H), maintenance(H, T).

% 7. Regional capacity: Total demand served by each regional warehouse cannot exceed its capacity
% Calculate total demand served by each regional
total_regional_demand(R) = #sum { D, C : customer_delivery(C, R, _), demand(C, D) }.
:- open_regional(R), total_regional_demand(R) > regional_capacity(R).

% 8. Hub capacity: Total demand passing through each hub cannot exceed hub capacity
% Calculate total demand through each hub (sum of demands at all supplied regional warehouses)
total_hub_demand(H) = #sum { D, C : customer_delivery(C, R, _), hub_supply(R, H), demand(C, D) }.
:- open_hub(H), total_hub_demand(H) > hub_capacity(H).

% 9. Truck limits: Number of customer deliveries in each time slot from regional warehouses supplied by a hub
% cannot exceed the hub's available trucks for that time slot
% Count deliveries per hub per time slot
deliveries_per_hub_time(H, T) = #count { C : customer_delivery(C, R, T), hub_supply(R, H) }.
:- open_hub(H), time(T), deliveries_per_hub_time(H, T) > truck_limit(H, T).

% ==================== COST CALCULATION ====================
% Fixed opening costs
fixed_cost = #sum { Cost, F : open_hub(F), opening_cost(F, Cost) }.
fixed_cost = #sum { Cost, F : open_regional(F), opening_cost(F, Cost) }.

% Hub-to-Regional transport costs
% For each hub_supply link, cost = total demand at regional × unit cost
hub_regional_cost = #sum { Cost, R, H : hub_supply(R, H), total_regional_demand(R), transport_cost(H, R, Cost) }.

% Regional-to-Customer transport costs
regional_customer_cost = #sum { Cost, C, R, T : customer_delivery(C, R, T), demand(C, D), transport_cost(R, C, Cost), Cost = D * Cost }.

% Total cost
total_cost = fixed_cost + hub_regional_cost + regional_customer_cost.

% ==================== OPTIMIZATION ====================
#minimize { total_cost }.

% ==================== SHOW DIRECTIVES ====================
#show open_hub/1.
#show open_regional/1.
#show hub_supply/2.
#show customer_delivery/3.
#show total_cost/0.