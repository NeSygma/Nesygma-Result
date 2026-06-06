% Maximum Flow with Budget and Flow Type Constraints

% Domain declarations
node(1..8).
edge_type(standard; premium).

% Priority nodes
priority_node(3).
priority_node(5).

% Edge definitions: edge(from, to, capacity, cost, type)
edge(1, 2, 10, 2, standard).
edge(1, 3, 12, 4, premium).
edge(2, 4, 8, 1, standard).
edge(2, 5, 4, 3, premium).
edge(3, 4, 5, 3, standard).
edge(3, 6, 10, 5, premium).
edge(4, 7, 10, 2, standard).
edge(5, 7, 7, 4, premium).
edge(6, 8, 12, 2, premium).
edge(7, 8, 15, 1, standard).

% Source and sink
source(1).
sink(8).

% Flow variables: flow on each edge (0 to capacity)
{ flow(F, T, V) : V = 0..Cap } :- edge(F, T, Cap, _, _).

% Capacity constraint: flow cannot exceed capacity
:- flow(F, T, V), edge(F, T, Cap, _, _), V > Cap.

% Flow conservation for intermediate nodes
% For each node N (not source/sink), incoming flow = outgoing flow
:- node(N), not source(N), not sink(N),
   incoming_flow_sum(N) != outgoing_flow_sum(N).

% Helper: incoming flow to node N
incoming_flow_sum(N) = #sum{ V, F : flow(F, N, V) } :- node(N).

% Helper: outgoing flow from node N
outgoing_flow_sum(N) = #sum{ V, T : flow(N, T, V) } :- node(N).

% Budget constraint: total cost ≤ 100
total_cost_sum = #sum{ Cost*V, F, T : flow(F, T, V), edge(F, T, _, Cost, _) }.
:- total_cost_sum > 100.

% Priority node rule: for priority nodes, if incoming > 0, then premium_outgoing ≥ 0.75 * outgoing
% First, calculate premium outgoing flow for priority nodes
premium_out_sum(N) = #sum{ V, T : flow(N, T, V), edge(N, T, _, _, premium) } :- priority_node(N).

% Rule: premium_outgoing ≥ 0.75 * outgoing_flow for priority nodes with incoming flow
:- priority_node(N), incoming_flow_sum(N) > 0,
   premium_out_sum(N) < 0.75 * outgoing_flow_sum(N).

% Global flow balancing: standard flow ≥ 50% of premium flow
% Calculate total standard and premium flows
total_std_sum = #sum{ V, F, T : flow(F, T, V), edge(F, T, _, _, standard) }.
total_prem_sum = #sum{ V, F, T : flow(F, T, V), edge(F, T, _, _, premium) }.

% Constraint: standard ≥ 0.5 * premium
:- total_std_sum < 0.5 * total_prem_sum.

% Total flow from source to sink
total_flow_sum = #sum{ V, T : flow(1, T, V) }.

% Objective: maximize total flow
#maximize { total_flow_sum }.

% Show relevant information
#show flow/3.
#show total_flow_sum/0.
#show total_cost_sum/0.
#show total_std_sum/0.
#show total_prem_sum/0.