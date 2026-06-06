% Domains
house(1..5).
color(red;green;white;yellow;blue).
nationality(brit;swede;dane;norwegian;german).
drink(tea;coffee;milk;beer;water).
cigarette(pallmall;dunhill;blends;bluemaster;prince).
pet(dog;birds;cats;horse;zebra).

% Exactly one attribute per house
1 { has_color(H,C) : color(C) } 1 :- house(H).
1 { has_nat(H,N) : nationality(N) } 1 :- house(H).
1 { has_drink(H,D) : drink(D) } 1 :- house(H).
1 { has_cig(H,S) : cigarette(S) } 1 :- house(H).
1 { has_pet(H,P) : pet(P) } 1 :- house(H).

% All-different constraints
:- has_color(H1,C), has_color(H2,C), H1 != H2.
:- has_nat(H1,N), has_nat(H2,N), H1 != H2.
:- has_drink(H1,D), has_drink(H2,D), H1 != H2.
:- has_cig(H1,S), has_cig(H2,S), H1 != H2.
:- has_pet(H1,P), has_pet(H2,P), H1 != H2.

% Neighbor definition (adjacent houses)
neighbor(H,N) :- house(H), house(N), N = H-1.
neighbor(H,N) :- house(H), house(N), N = H+1.

% Clues
% 1. Brit lives in red house
has_color(H,red) :- has_nat(H,brit).
% 2. Swede keeps dogs
has_pet(H,dog) :- has_nat(H,swede).
% 3. Dane drinks tea
has_drink(H,tea) :- has_nat(H,dane).
% 4. Green house is left of white house (directly adjacent)
:- has_color(H,green), H < 5, not has_color(H+1,white).
:- has_color(5,green). % green cannot be last house
% 5. Green house's owner drinks coffee
has_drink(H,coffee) :- has_color(H,green).
% 6. Pall Mall -> birds
has_pet(H,birds) :- has_cig(H,pallmall).
% 7. Yellow house -> Dunhill
has_cig(H,dunhill) :- has_color(H,yellow).
% 8. Center house drinks milk
has_drink(3,milk).
% 9. Norwegian lives in first house
has_nat(1,norwegian).
% 10. Blends neighbor cats
:- has_cig(H,blends), neighbor(H,N), not has_pet(N,cats).
% 11. Horse neighbor Dunhill
:- has_pet(H,horse), neighbor(H,N), not has_cig(N,dunhill).
% 12. Blue Master drinks beer
has_drink(H,beer) :- has_cig(H,bluemaster).
% 13. German smokes Prince
has_cig(H,prince) :- has_nat(H,german).
% 14. Norwegian next to blue house
:- has_nat(H,norwegian), neighbor(H,N), not has_color(N,blue).
% 15. Blends neighbor water drinker
:- has_cig(H,blends), neighbor(H,N), not has_drink(N,water).

% Zebra owner
zebra_owner(N) :- has_pet(H,zebra), has_nat(H,N).

#show has_color/2.
#show has_nat/2.
#show has_drink/2.
#show has_cig/2.
#show has_pet/2.
#show zebra_owner/1.