% Domain
bay(1..6).
cargo(fuel; grain; livestock; machinery; produce; textiles).

% Each bay gets exactly one cargo, each cargo assigned to exactly one bay
1 { assignment(B, C) : bay(B) } 1 :- cargo(C).
1 { assignment(B, C) : cargo(C) } 1 :- bay(B).

% Constraints
% grain > livestock
:- assignment(G, grain), assignment(L, livestock), G <= L.

% livestock > textiles
:- assignment(L, livestock), assignment(T, textiles), L <= T.

% produce > fuel
:- assignment(P, produce), assignment(F, fuel), P <= F.

% textiles is next to produce
:- assignment(T, textiles), assignment(P, produce), |T - P| != 1.

% Q: exactly one bay between machinery and grain
:- assignment(M, machinery), assignment(G, grain), |M - G| != 2.

#show assignment/2.