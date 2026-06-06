% Genes
gene(g1). gene(g2). gene(g3). gene(g4). gene(g5).

% Each gene has exactly one state 0 or 1
1 { state(G,0); state(G,1) } 1 :- gene(G).

% Constitutive expression
state(g4,1). state(g5,1). state(g3,1).

% Complementary regulation between g1 and g2
:- state(g1,1), state(g2,1).
:- state(g1,0), state(g2,0).

#show state/2.