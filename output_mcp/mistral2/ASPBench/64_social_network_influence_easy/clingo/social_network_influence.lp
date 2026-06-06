% --- Facts ---
user(user1; user2; user3; user4; user5; user6; user7; user8).

% User properties: user(User, InfluenceWeight, Cost, Category)
user(user1, 0.8, 100, influencer).
user(user2, 0.3, 50, regular).
user(user3, 0.5, 80, regular).
user(user4, 0.9, 150, influencer).
user(user5, 0.4, 60, regular).
user(user6, 0.6, 90, regular).
user(user7, 0.7, 120, influencer).
user(user8, 0.2, 40, regular).

% Connections: conn(From, To, Strength)
conn(user1, user2, 0.6).
conn(user1, user3, 0.7).
conn(user2, user3, 0.4).
conn(user2, user5, 0.5).
conn(user3, user4, 0.3).
conn(user4, user5, 0.8).
conn(user4, user6, 0.6).
conn(user5, user7, 0.5).
conn(user6, user7, 0.7).
conn(user7, user8, 0.4).

% Budget and constraints
total_budget(300).
max_seeds(2).

% --- Choice Rule: Select seeds ---
1 { selected_seed(U) : user(U, _, _, _) } 2.

% --- Budget Constraint ---
total_cost(C) :- C = #sum { Cost, U : selected_seed(U), user(U, _, Cost, _) }.
:- total_cost(C), total_budget(B), C > B.

% --- Direct Influence ---
directly_influenced(U) :-
    selected_seed(S),
    conn(S, U, Strength),
    Strength >= 0.3.

% --- Secondary Influence ---
secondary_influenced(U) :-
    directly_influenced(D),
    conn(D, U, Strength),
    Strength >= 0.2,
    not selected_seed(U),
    not directly_influenced(U).

% --- Exclusivity: Ensure no overlap between direct and secondary ---
:- directly_influenced(U), secondary_influenced(U).

% --- Total Reach ---
total_reach(N) :-
    N = #count { U : selected_seed(U) } +
        #count { U : directly_influenced(U) } +
        #count { U : secondary_influenced(U) }.

% --- Objective: Maximize total_reach ---
#maximize { N : total_reach(N) }.

% --- Show selected seeds and influenced users ---
#show selected_seed/1.
#show directly_influenced/1.
#show secondary_influenced/1.
#show total_reach/1.
#show total_cost/1.