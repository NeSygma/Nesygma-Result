% Domains
space(1..7).
business(optometrist).
business(pharmacy).
business(restaurant1).
business(restaurant2).
business(shoe_store).
business(toy_store).
business(veterinarian).

% Each business occupies exactly one space
1 { assign(B, S) : space(S) } 1 :- business(B).

% Each space has exactly one business
1 { assign(B, S) : business(B) } 1 :- space(S).

% Constraint 1: Pharmacy at one end, one restaurant at the other
assign(pharmacy, 1) | assign(pharmacy, 7).
assign(restaurant1, 1) | assign(restaurant1, 7) | assign(restaurant2, 1) | assign(restaurant2, 7).

% Constraint 2: Two restaurants must be separated by at least 2 other businesses
:- assign(restaurant1, S1), assign(restaurant2, S2), |S1 - S2| < 3.

% Constraint 3: Pharmacy must be next to either optometrist or veterinarian
:- assign(pharmacy, S), not next_to(pharmacy, optometrist), not next_to(pharmacy, veterinarian).

% Helper: next_to relation
next_to(B1, B2) :- assign(B1, S1), assign(B2, S2), |S1 - S2| = 1.

% Constraint 4: Toy store cannot be next to veterinarian
:- next_to(toy_store, veterinarian).

% Question condition: optometrist is next to shoe store
opt_next_shoe :- next_to(optometrist, shoe_store).

% Find what businesses are immediately on either side of the optometrist-shoe store pair
% If optometrist and shoe store are adjacent, they occupy two consecutive spaces
% The businesses on either side would be at positions S-1 and S+2 (or S-2 and S+1)

% Let's find all valid arrangements where optometrist is next to shoe store
% Then check what must be on either side

% We need to find what is forced to be on either side when opt_next_shoe holds
% Let's define the pair positions
pair_left(S) :- assign(optometrist, S), assign(shoe_store, S+1).
pair_right(S) :- assign(optometrist, S+1), assign(shoe_store, S).

% The businesses on either side would be at S-1 and S+2 (if pair_left) or S-2 and S+1 (if pair_right)
left_business(B, S) :- pair_left(S), assign(B, S-1), space(S-1).
right_business(B, S) :- pair_left(S), assign(B, S+2), space(S+2).
left_business(B, S) :- pair_right(S), assign(B, S-2), space(S-2).
right_business(B, S) :- pair_right(S), assign(B, S+1), space(S+1).

% Now we need to check which answer choices are always true when opt_next_shoe holds
% We'll create atoms for each option condition

% Option A: pharmacy and a restaurant
option_a_holds :- opt_next_shoe, 
                  left_business(pharmacy, _), 
                  left_business(restaurant1, _).
option_a_holds :- opt_next_shoe, 
                  left_business(pharmacy, _), 
                  left_business(restaurant2, _).
option_a_holds :- opt_next_shoe, 
                  right_business(pharmacy, _), 
                  right_business(restaurant1, _).
option_a_holds :- opt_next_shoe, 
                  right_business(pharmacy, _), 
                  right_business(restaurant2, _).

% Option B: pharmacy and toy store
option_b_holds :- opt_next_shoe, 
                  left_business(pharmacy, _), 
                  left_business(toy_store, _).
option_b_holds :- opt_next_shoe, 
                  right_business(pharmacy, _), 
                  right_business(toy_store, _).

% Option C: two restaurants
option_c_holds :- opt_next_shoe, 
                  left_business(restaurant1, _), 
                  right_business(restaurant2, _).
option_c_holds :- opt_next_shoe, 
                  left_business(restaurant2, _), 
                  right_business(restaurant1, _).

% Option D: restaurant and toy store
option_d_holds :- opt_next_shoe, 
                  left_business(restaurant1, _), 
                  right_business(toy_store, _).
option_d_holds :- opt_next_shoe, 
                  left_business(restaurant2, _), 
                  right_business(toy_store, _).
option_d_holds :- opt_next_shoe, 
                  right_business(restaurant1, _), 
                  left_business(toy_store, _).
option_d_holds :- opt_next_shoe, 
                  right_business(restaurant2, _), 
                  left_business(toy_store, _).

% Option E: restaurant and veterinarian
option_e_holds :- opt_next_shoe, 
                  left_business(restaurant1, _), 
                  right_business(veterinarian, _).
option_e_holds :- opt_next_shoe, 
                  left_business(restaurant2, _), 
                  right_business(veterinarian, _).
option_e_holds :- opt_next_shoe, 
                  right_business(restaurant1, _), 
                  left_business(veterinarian, _).
option_e_holds :- opt_next_shoe, 
                  right_business(restaurant2, _), 
                  left_business(veterinarian, _).

% We need to find which option is ALWAYS true when opt_next_shoe holds
% We'll use a different approach: find all valid arrangements with opt_next_shoe
% and see which option holds in ALL of them

% First, let's find all valid arrangements
valid_arrangement :- assign(_, _), opt_next_shoe.

% Count how many arrangements satisfy each option
count_a(N) :- N = #count{1 : valid_arrangement, option_a_holds}.
count_b(N) :- N = #count{1 : valid_arrangement, option_b_holds}.
count_c(N) :- N = #count{1 : valid_arrangement, option_c_holds}.
count_d(N) :- N = #count{1 : valid_arrangement, option_d_holds}.
count_e(N) :- N = #count{1 : valid_arrangement, option_e_holds}.

% Total valid arrangements
total_arrangements(N) :- N = #count{1 : valid_arrangement}.

% An option is always true if its count equals total arrangements
always_a :- count_a(N), total_arrangements(N).
always_b :- count_b(N), total_arrangements(N).
always_c :- count_c(N), total_arrangements(N).
always_d :- count_d(N), total_arrangements(N).
always_e :- count_e(N), total_arrangements(N).

% Map to answer options
option(a) :- always_a.
option(b) :- always_b.
option(c) :- always_c.
option(d) :- always_d.
option(e) :- always_e.

#show option/1.