fof(premise1, axiom,
    ! [X] : ((rabbit(X) & can_be_spotted_near_campus(X)) => cute(X))).

fof(premise2, axiom,
    ? [X] : (turtle(X) & can_be_spotted_near_campus(X))).

fof(premise3, axiom,
    ! [X] : (can_be_spotted_near_campus(X) => (rabbit(X) | squirrel(X)))).

fof(premise4, axiom,
    ! [X] : (skittish(X) => ~calm(X))).

fof(premise5, axiom,
    ! [X] : ((squirrel(X) & can_be_spotted_near_campus(X)) => skittish(X))).

fof(premise6, axiom,
    can_be_spotted_near_campus(rockie) & calm(rockie)).

fof(conclusion, conjecture,
    turtle(rockie) | cute(rockie)).