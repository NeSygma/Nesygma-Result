%% ============================================================
%% Combinatorial Auction with Synergy Bonuses
%% ============================================================

%% --- Domain Facts ---

%% Bidders: bidder(Name, Budget, SynergyBonus)
bidder(a, 150, 20).
bidder(b, 200, 10).
bidder(c, 180, 25).
bidder(d, 100, 5).

%% Items: item(Name, Category)
item(item1, electronics).
item(item2, electronics).
item(item3, furniture).
item(item4, furniture).
item(item5, electronics).
item(item6, furniture).
item(lic_E, license).
item(lic_F, license).

%% Bids: bid(ID, Bidder, Price)
bid(1, a, 70).
bid(2, a, 40).
bid(3, b, 90).
bid(4, b, 50).
bid(5, b, 60).
bid(6, c, 100).
bid(7, c, 60).
bid(8, c, 80).
bid(9, d, 25).
bid(10, d, 70).

%% Bid items: bid_item(BidID, Item)
bid_item(1, item1).
bid_item(1, item2).
bid_item(2, lic_E).
bid_item(3, item3).
bid_item(3, item4).
bid_item(4, lic_F).
bid_item(5, item5).
bid_item(6, item1).
bid_item(6, item5).
bid_item(7, lic_E).
bid_item(8, item3).
bid_item(8, item6).
bid_item(9, lic_F).
bid_item(10, item4).

%% --- Decision: which bids win ---
{ win(B) } :- bid(B, _, _).

%% --- Constraint 1: Item Exclusivity ---
%% Each item can appear in at most one winning bid.
:- win(B1), win(B2), B1 != B2,
   bid_item(B1, I), bid_item(B2, I).

%% --- Constraint 2: Budget Compliance ---
%% Total price of all bids won by a bidder cannot exceed their budget.
total_price(Bidder, Total) :-
    bidder(Bidder, Budget, _),
    Total = #sum { P, B : win(B), bid(B, Bidder, P) },
    Total <= Budget.

%% Actually enforce: sum of prices for each bidder <= budget
:- bidder(Bidder, Budget, _),
   #sum { P, B : win(B), bid(B, Bidder, P) } > Budget.

%% --- Constraint 3: Synergy Bonus ---
%% If a bidder wins two or more bids, their synergy bonus is added.
multiple_wins(Bidder) :- bidder(Bidder, _, _),
    #count { B : win(B), bid(B, Bidder, _) } >= 2.

%% --- Constraint 4: Licensing Requirement ---
%% To win any bid containing items from a category (electronics or furniture),
%% the bidder must also win a separate bid for the corresponding license.

%% A bidder wins items of a category if they win a bid containing such an item
wins_category_item(Bidder, Cat) :-
    win(B), bid(B, Bidder, _),
    bid_item(B, I),
    item(I, Cat),
    Cat != license.

%% A bidder wins a license bid
wins_license(Bidder, LicItem) :-
    win(B), bid(B, Bidder, _),
    bid_item(B, LicItem),
    item(LicItem, license).

%% For electronics: need lic_E
:- wins_category_item(Bidder, electronics),
   not wins_license(Bidder, lic_E).

%% For furniture: need lic_F
:- wins_category_item(Bidder, furniture),
   not wins_license(Bidder, lic_F).

%% --- Constraint 5: Fairness Constraint ---
%% No single bidder can be allocated more than 3 items total across all winning bids.
total_items(Bidder, Total) :-
    bidder(Bidder, _, _),
    Total = #count { I, B : win(B), bid(B, Bidder, _), bid_item(B, I), item(I, _), I != lic_E, I != lic_F }.

:- total_items(Bidder, Total), Total > 3.

%% --- Objective: Maximize total revenue ---
%% Total revenue = sum of winning bid prices + synergy bonuses for multiple winners
total_bid_price(Total) :-
    Total = #sum { P, B : win(B), bid(B, _, P) }.

total_synergy(Total) :-
    Total = #sum { Bonus, Bidder : multiple_wins(Bidder), bidder(Bidder, _, Bonus) }.

total_revenue(R) :-
    total_bid_price(P),
    total_synergy(S),
    R = P + S.

%% Maximize total revenue
#maximize { R : total_revenue(R) }.

%% --- Output ---
#show win/1.
#show total_revenue/1.
#show multiple_wins/1.