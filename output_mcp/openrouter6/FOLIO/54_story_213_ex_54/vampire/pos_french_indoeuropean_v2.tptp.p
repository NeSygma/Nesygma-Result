fof(premise_1, axiom, ! [X] : (Romance(X) => IndoEuropean(X))).

fof(premise_2, axiom, Romance(french) & Romance(spanish)).

fof(premise_3, axiom, Related(german, spanish)).

fof(premise_4, axiom, ! [X] : (X != basque => ~Related(basque, X))).

fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).

fof(goal, conjecture, IndoEuropean(french)).