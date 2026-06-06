% --- Domains ---
hub(h1; h2).
regional(r1; r2; r3; r4).
customer(c1; c2; c3; c4; c5; c6).
time(1..4).

% --- Instance Data ---
% Opening costs
opening_cost_hub(h1, 1000).
opening_cost_hub(h2, 1200).
opening_cost_regional(r1, 200).
opening_cost_regional(r2, 250).
opening_cost_regional(r3, 220).
opening_cost_regional(r4, 180).

% Capacities
hub_capacity(h1, 400).
hub_capacity(h2, 350).
regional_capacity(r1, 70).
regional_capacity(r2, 80).
regional_capacity(r3, 60).
regional_capacity(r4, 90).

% Truck limits per time slot
hub_truck_limit(h1, 1, 2).
hub_truck_limit(h1, 2, 2).
hub_truck_limit(h1, 3, 2).
hub_truck_limit(h1, 4, 2).
hub_truck_limit(h2, 1, 1).
hub_truck_limit(h2, 2, 1).
hub_truck_limit(h2, 3, 1).
hub_truck_limit(h2, 4, 1).

% Customer demands
demand(c1, 20).
demand(c2, 30).
demand(c3, 15).
demand(c4, 25).
demand(c5, 35).
demand(c6, 10).

% Time windows
time_window(c1, 2, 3).
time_window(c2, 1, 2).
time_window(c3, 3, 4).
time_window(c4, 1, 4).
time_window(c5, 2, 4).
time_window(c6, 1, 1).

% Transportation costs
% Hub to Regional
hub_to_regional_cost(h1, r1, 5).
hub_to_regional_cost(h1, r2, 6).
hub_to_regional_cost(h2, r3, 5).
hub_to_regional_cost(h2, r4, 6).

% Regional to Customer
regional_to_customer_cost(r1, c1, 10).
regional_to_customer_cost(r1, c2, 12).
regional_to_customer_cost(r2, c2, 13).
regional_to_customer_cost(r2, c3, 15).
regional_to_customer_cost(r3, c4, 9).
regional_to_customer_cost(r3, c5, 11).
regional_to_customer_cost(r4, c5, 14).
regional_to_customer_cost(r4, c6, 7).

% Connectivity
hub_supplies(h1, r1).
hub_supplies(h1, r2).
hub_supplies(h2, r3).
hub_supplies(h2, r4).

regional_serves(r1, c1).
regional_serves(r1, c2).
regional_serves(r2, c2).
regional_serves(r2, c3).
regional_serves(r3, c4).
regional_serves(r3, c5).
regional_serves(r4, c5).
regional_serves(r4, c6).

% Maintenance
maintenance(r2, 2).
maintenance_hub(h1, 4).

% --- Choice Rules ---
{ open_hub(H) } :- hub(H).
{ open_regional(R) } :- regional(R).
{ supplied_by(R, H) : hub(H) } 1 :- open_regional(R).
{ delivery(C, R, T) : regional(R), time(T) } 1 :- customer(C).

% --- Constraints ---
% Opening prerequisite: open regional must be supplied by open hub
:- open_regional(R), supplied_by(R, H), not open_hub(H).

% Supply uniqueness: each open regional must be supplied by exactly one hub
:- open_regional(R), not 1 { supplied_by(R, H) : hub(H) } 1.

% Connectivity constraints
:- supplied_by(R, H), not hub_supplies(H, R).
:- delivery(C, R, _), not regional_serves(R, C).

% Time window constraints
:- delivery(C, R, T), time_window(C, Start, End), T < Start.
:- delivery(C, R, T), time_window(C, Start, End), T > End.

% Maintenance constraints
:- delivery(C, R, T), maintenance(R, T).
:- delivery(C, R, T), maintenance_hub(H, T), supplied_by(R, H).

% Regional capacity constraints
:- open_regional(R), #sum { Demand : delivery(C, R, _), demand(C, Demand) } > Capacity, regional_capacity(R, Capacity).

% Hub capacity constraints
:- open_hub(H), #sum { Demand : delivery(C, R, _), supplied_by(R, H), demand(C, Demand) } > Capacity, hub_capacity(H, Capacity).

% Truck limit constraints
:- open_hub(H), time(T), #count { C : delivery(C, R, T), supplied_by(R, H) } > Limit, hub_truck_limit(H, T, Limit).

% --- Cost Calculation ---
% Fixed opening costs
fixed_cost(Fixed) :-
    Fixed = #sum { OpeningCost : open_hub(H), opening_cost_hub(H, OpeningCost) }
    + #sum { OpeningCost : open_regional(R), opening_cost_regional(R, OpeningCost) }.

% Hub-to-Regional transport costs
supply_demand(R, Demand) :-
    Demand = #sum { D : delivery(C, R, _), demand(C, D) }.

hub_to_regional_transport_cost(HubToRegional) :-
    HubToRegional = #sum {
        Supply*UnitCost : supplied_by(R, H),
                          supply_demand(R, Supply),
                          hub_to_regional_cost(H, R, UnitCost)
    }.

% Regional-to-Customer transport costs
regional_to_customer_transport_cost(RegionalToCustomer) :-
    RegionalToCustomer = #sum {
        Demand*UnitCost : delivery(C, R, _),
                          demand(C, Demand),
                          regional_to_customer_cost(R, C, UnitCost)
    }.

% Total cost
total_cost(Cost) :-
    Cost = Fixed + HubToRegional + RegionalToCustomer,
    fixed_cost(Fixed),
    hub_to_regional_transport_cost(HubToRegional),
    regional_to_customer_transport_cost(RegionalToCustomer).

% --- Optimization ---
#minimize { Cost : total_cost(Cost) }.

% --- Show directives ---
#show open_hub/1.
#show open_regional/1.
#show supplied_by/2.
#show delivery/3.
#show total_cost/1.