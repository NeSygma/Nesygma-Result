% --- Data ---
bidder(a; b; c; d).
budget(a, 150). budget(b, 200). budget(c, 180). budget(d, 100).
synergy_bonus(a, 20). synergy_bonus(b, 10). synergy_bonus(c, 25). synergy_bonus(d, 5).

item(item1; item2; item3; item4; item5; item6; lic_E; lic_F).
category(item1, electronics). category(item2, electronics). category(item5, electronics).
category(item3, furniture). category(item4, furniture). category(item6, furniture).
category(lic_E, license_electronics). category(lic_F, license_furniture).

% Bid definitions
bid(1, a, 70). item_in_bid(1, item1). item_in_bid(1, item2).
bid(2, a, 40). item_in_bid(2, lic_E).
bid(3, b, 90). item_in_bid(3, item3). item_in_bid(3, item4).
bid(4, b, 50). item_in_bid(4, lic_F).
bid(5, b, 60). item_in_bid(5, item5).
bid(6, c, 100). item_in_bid(6, item1). item_in_bid(6, item5).
bid(7, c, 60). item_in_bid(7, lic_E).
bid(8, c, 80). item_in_bid(8, item3). item_in_bid(8, item6).
bid(9, d, 25). item_in_bid(9, lic_F).
bid(10, d, 70). item_in_bid(10, item4).

% --- Logic ---
{ win(BidID) } :- bid(BidID, _, _).

% Item allocation
item_allocated(Item, Bidder) :- win(BidID), bid(BidID, Bidder, _), item_in_bid(BidID, Item).

% 1. Item Exclusivity
:- item_allocated(Item, B1), item_allocated(Item, B2), B1 != B2.

% 2. Budget Compliance
bidder_total_price(Bidder, S) :- bidder(Bidder), S = #sum { P, BidID : win(BidID), bid(BidID, Bidder, P) }.
:- bidder(Bidder), bidder_total_price(Bidder, S), budget(Bidder, B), S > B.

% 3. Synergy Bonus
bidder_wins_count(Bidder, C) :- bidder(Bidder), C = #count { BidID : win(BidID), bid(BidID, Bidder, _) }.
has_synergy(Bidder) :- bidder_wins_count(Bidder, C), C >= 2.

% 4. Licensing Requirement
has_electronics(Bidder) :- win(BidID), bid(BidID, Bidder, _), item_in_bid(BidID, Item), category(Item, electronics).
has_furniture(Bidder) :- win(BidID), bid(BidID, Bidder, _), item_in_bid(BidID, Item), category(Item, furniture).
has_lic_E(Bidder) :- win(BidID), bid(BidID, Bidder, _), item_in_bid(BidID, lic_E).
has_lic_F(Bidder) :- win(BidID), bid(BidID, Bidder, _), item_in_bid(BidID, lic_F).

:- has_electronics(Bidder), not has_lic_E(Bidder).
:- has_furniture(Bidder), not has_lic_F(Bidder).

% 5. Fairness Constraint
bidder_total_items(Bidder, N) :- bidder(Bidder), N = #count { Item : item_allocated(Item, Bidder) }.
:- bidder(Bidder), bidder_total_items(Bidder, N), N > 3.

% Objective
total_revenue(R) :- R = #sum { P, BidID : win(BidID), bid(BidID, _, P); SB, Bidder : has_synergy(Bidder), synergy_bonus(Bidder, SB) }.

#maximize { R : total_revenue(R) }.

#show win/1.
#show total_revenue/1.