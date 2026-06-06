% --- Data Facts ---

% Bidders with budgets and synergy bonuses
bidder(a;b;c;d).
budget(a,150). budget(b,200). budget(c,180). budget(d,100).
synergy_bonus(a,20). synergy_bonus(b,10). synergy_bonus(c,25). synergy_bonus(d,5).

% Items
item(item1;item2;item3;item4;item5;item6;lic_E;lic_F).

% Categories
category(item1,electronics). category(item2,electronics). category(item5,electronics).
category(item3,furniture). category(item4,furniture). category(item6,furniture).
category(lic_E,license). category(lic_F,license).

% Bids
bid(1..10).
bid_bidder(1,a). bid_bidder(2,a). bid_bidder(3,b). bid_bidder(4,b). bid_bidder(5,b).
bid_bidder(6,c). bid_bidder(7,c). bid_bidder(8,c). bid_bidder(9,d). bid_bidder(10,d).

bid_price(1,70). bid_price(2,40). bid_price(3,90). bid_price(4,50). bid_price(5,60).
bid_price(6,100). bid_price(7,60). bid_price(8,80). bid_price(9,25). bid_price(10,70).

% Bid items
bid_item(1,item1). bid_item(1,item2).
bid_item(2,lic_E).
bid_item(3,item3). bid_item(3,item4).
bid_item(4,lic_F).
bid_item(5,item5).
bid_item(6,item1). bid_item(6,item5).
bid_item(7,lic_E).
bid_item(8,item3). bid_item(8,item6).
bid_item(9,lic_F).
bid_item(10,item4).

% --- Decision Variable ---

% Choose which bids win
{ win(B) } :- bid(B).

% --- Constraint 1: Item Exclusivity ---
% Each item can appear in at most one winning bid
:- win(B1), win(B2), B1 != B2, bid_item(B1,I), bid_item(B2,I).

% --- Constraint 2: Budget Compliance ---
% Total price of all bids won by a bidder cannot exceed their budget
total_bidder_price(Bidder, Total) :-
    bidder(Bidder),
    Total = #sum { P, B : win(B), bid_bidder(B,Bidder), bid_price(B,P) }.
:- total_bidder_price(Bidder, Total), budget(Bidder, Budget), Total > Budget.

% --- Constraint 3: Synergy Bonus ---
% If a bidder wins 2 or more bids, their synergy bonus is added
win_count(Bidder, Count) :-
    bidder(Bidder),
    Count = #count { B : win(B), bid_bidder(B,Bidder) }.

synergy_applies(Bidder) :- win_count(Bidder, Count), Count >= 2.

% --- Constraint 4: Licensing Requirement ---
% A bidder who wins electronics items must also win lic_E
wins_electronics(Bidder) :- win(B), bid_bidder(B,Bidder), bid_item(B,I), category(I,electronics).
wins_furniture(Bidder) :- win(B), bid_bidder(B,Bidder), bid_item(B,I), category(I,furniture).

% Must win the corresponding license
wins_lic_E(Bidder) :- win(B), bid_bidder(B,Bidder), bid_item(B,lic_E).
wins_lic_F(Bidder) :- win(B), bid_bidder(B,Bidder), bid_item(B,lic_F).

:- wins_electronics(Bidder), not wins_lic_E(Bidder).
:- wins_furniture(Bidder), not wins_lic_F(Bidder).

% --- Constraint 5: Fairness Constraint ---
% No single bidder can be allocated more than 3 items total
total_items(Bidder, Total) :-
    bidder(Bidder),
    Total = #count { I, B : win(B), bid_bidder(B,Bidder), bid_item(B,I), item(I) }.
:- total_items(Bidder, Total), Total > 3.

% --- Objective: Maximize Total Revenue ---
% Revenue from winning bid prices
total_bid_revenue(Total) :-
    Total = #sum { P, B : win(B), bid_price(B,P) }.

% Revenue from synergy bonuses
total_synergy_revenue(Total) :-
    Total = #sum { Bonus, Bidder : synergy_applies(Bidder), synergy_bonus(Bidder,Bonus) }.

% Combined total revenue
total_revenue(R) :-
    total_bid_revenue(B),
    total_synergy_revenue(S),
    R = B + S.

% Maximize total revenue
#maximize { R@1 : total_revenue(R) }.

% --- Output ---
#show win/1.
#show total_revenue/1.
#show synergy_applies/1.