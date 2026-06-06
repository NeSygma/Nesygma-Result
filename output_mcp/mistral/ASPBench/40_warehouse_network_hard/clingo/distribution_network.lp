% --- DOMAIN DECLARATIONS ---
% Time slots
time(1..4).

% Hubs
hub(h1). hub(h2).

% Regional warehouses
regional(r1). regional(r2). regional(r3). regional(r4).

% Customers
customer(c1). customer(c2). customer(c3). customer(c4). customer(c5). customer(c6).

% --- INPUT DATA AS FACTS ---

% Opening costs
opening_cost(hub, h1, 1000).
opening_cost(hub, h2, 1200).
opening_cost(regional, r1, 200).
opening_cost(regional, r2, 250).
opening_cost(regional, r3, 220).
opening_cost(regional, r4, 180).

% Capacities
hub_capacity(h1, 400).
hub_capacity(h2, 350).
regional_capacity(r1, 70).
regional_capacity(r2, 80).
regional_capacity(r3, 60).
regional_capacity(r4, 90).

% Truck resources per hub per time slot
truck_resources(h1, 2).
truck_resources(h2, 1).

% Customer demands and time windows
customer_demand(c1, 20). customer_demand(c2, 30). customer_demand(c3, 15).
customer_demand(c4, 25). customer_demand(c5, 35). customer_demand(c6, 10).

time_window(c1, 2, 3).
time_window(c2, 1, 2).
time_window(c3, 3, 4).
time_window(c4, 1, 4).
time_window(c5, 2, 4).
time_window(c6, 1, 1).

% Transportation costs (per unit of demand)
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

% Connectivity constraints
% Hub can supply Regional Warehouse
hub_supply(h1, r1). hub_supply(h1, r2).
hub_supply(h2, r3). hub_supply(h2, r4).

% Regional Warehouse can serve Customer
regional_serve(r1, c1). regional_serve(r1, c2).
regional_serve(r2, c2). regional_serve(r2, c3).
regional_serve(r3, c4). regional_serve(r3, c5).
regional_serve(r4, c5). regional_serve(r4, c6).

% Maintenance schedules
% Facilities unavailable during specific time slots
unavailable(h1, 4).
unavailable(r2, 2).

% --- DECISION VARIABLES ---

% Which hubs are opened
{ open_hub(H) : hub(H) }.

% Which regional warehouses are opened
{ open_regional(R) : regional(R) }.

% Which hub supplies which regional warehouse (only if both are open)
{ supply_hub_to_regional(H, R) : hub_supply(H, R) } :- open_hub(H), open_regional(R).

% Which regional warehouse serves which customer at which time slot
% Only if the regional warehouse is open and can serve the customer
{ delivery(C, R, T) : regional_serve(R, C), time(T) } :-
    open_regional(R),
    customer(C),
    time(T),
    time_window(C, Tmin, Tmax),
    T >= Tmin,
    T =< Tmax.

% --- CONSTRAINTS ---

% 1. Opening prerequisite: A customer can only be served by an open regional warehouse,
%    which must be supplied by an open hub (enforced by the delivery rule above)

% 2. Assignment uniqueness: Each customer must be assigned to exactly one regional warehouse at exactly one time slot
:- customer(C), not 1 { delivery(C, R, T) : regional(R), time(T) } 1.

% 3. Supply uniqueness: Each open regional warehouse must be supplied by exactly one hub
:- open_regional(R), not 1 { supply_hub_to_regional(H, R) : hub(H) } 1.

% 4. Connectivity: Already enforced by the supply_hub_to_regional and delivery choice rules

% 5. Time windows: Already enforced in the delivery choice rule

% 6. Maintenance: No deliveries can pass through facilities during their maintenance time slots
%    This means no delivery can occur at a time slot when the regional warehouse is unavailable
:- delivery(C, R, T), unavailable(R, T).

% 7. Regional capacity: Total demand served by each regional warehouse cannot exceed its capacity
:- open_regional(R),
   #sum { D : delivery(C, R, T), customer_demand(C, D) } > regional_capacity(R, _).

% 8. Hub capacity: Total demand passing through each hub cannot exceed hub capacity
%    Demand passing through a hub = sum of demands at all regional warehouses it supplies
:- open_hub(H),
   #sum { D : supply_hub_to_regional(H, R), delivery(C, R, T), customer_demand(C, D) } > hub_capacity(H, _).

% 9. Truck limits: Number of customer deliveries in each time slot from regional warehouses
%    supplied by a hub cannot exceed the hub's available trucks for that time slot
:- open_hub(H),
   time(T),
   #count { C, R : delivery(C, R, T), supply_hub_to_regional(H, R) } > truck_resources(H, _).

% --- COST CALCULATION ---

% Fixed opening costs
fixed_cost(C) :- open_hub(H), opening_cost(hub, H, C).
fixed_cost(C) :- open_regional(R), opening_cost(regional, R, C).

total_fixed_cost(F) :-
    F = #sum { C : fixed_cost(C) }.

% Hub-to-Regional transport costs = sum over all supply links of (regional warehouse's total demand × hub-to-regional unit cost)
regional_demand(R, D) :-
    open_regional(R),
    D = #sum { Dc : delivery(C, R, T), customer_demand(C, Dc) }.

hub_to_regional_transport_cost(Cost) :-
    supply_hub_to_regional(H, R),
    regional_demand(R, D),
    hub_to_regional_cost(H, R, U),
    Cost = D * U.

total_hub_to_regional_cost(THRC) :-
    THRC = #sum { Cost : hub_to_regional_transport_cost(Cost) }.

% Regional-to-Customer transport costs = sum over all deliveries of (customer demand × regional-to-customer unit cost)
regional_to_customer_transport_cost(Cost) :-
    delivery(C, R, T),
    customer_demand(C, D),
    regional_to_customer_cost(R, C, U),
    Cost = D * U.

total_regional_to_customer_cost(TRCC) :-
    TRCC = #sum { Cost : regional_to_customer_transport_cost(Cost) }.

total_cost(Total) :-
    total_fixed_cost(F),
    total_hub_to_regional_cost(HRC),
    total_regional_to_customer_cost(RCC),
    Total = F + HRC + RCC.

% --- OPTIMIZATION ---
#minimize { Total : total_cost(Total) }.

% --- OUTPUT ---
#show open_hub/1.
#show open_regional/1.
#show supply_hub_to_regional/2.
#show delivery/3.
#show total_cost/1.