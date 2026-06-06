% Combinatorial Auction Mechanism in Clingo ASP

% ==================== DOMAIN DEFINITIONS ====================
% Bidders with budgets and synergy bonuses
bidder(a). bidder(b). bidder(c). bidder(d).
budget(a, 150). budget(b, 200). budget(c, 180). budget(d, 100).
synergy_bonus(a, 20). synergy_bonus(b, 10). synergy_bonus(c, 25). synergy_bonus(d, 5).

% Items with categories
item(item1). item(item2). item(item3). item(item4). item(item5). item(item6). item(lic_E). item(lic_F).
category(item1, electronics). category(item2, electronics). category(item5, electronics).
category(item3, furniture). category(item4, furniture). category(item6, furniture).
category(lic_E, license_e). category(lic_F, license_f).

% Bids: bid(id, bidder, price)
bid(1, a, 70). bid(2, a, 40). bid(3, b, 90). bid(4, b, 50). bid(5, b, 60).
bid(6, c, 100). bid(7, c, 60). bid(8, c, 80). bid(9, d, 25). bid(10, d, 70).

% Bid items: bid_items(bid_id, item)
bid_items(1, item1). bid_items(1, item2).
bid_items(2, lic_E).
bid_items(3, item3). bid_items(3, item4).
bid_items(4, lic_F).
bid_items(5, item5).
bid_items(6, item1). bid_items(6, item5).
bid_items(7, lic_E).
bid_items(8, item3). bid_items(8, item6).
bid_items(9, lic_F).
bid_items(10, item4).

% ==================== DECISION VARIABLES ====================
% Choose which bids are winning
{ winning_bid(B) } :- bid(B, _, _).

% ==================== CONSTRAINTS ====================

% 1. Item Exclusivity: Each item can appear in at most one winning bid
:- winning_bid(B1), winning_bid(B2), B1 != B2, bid_items(B1, I), bid_items(B2, I).

% 2. Budget Compliance: Total price of winning bids per bidder <= budget
% First, compute total spent per bidder
total_spent(Bidder, Total) :- bidder(Bidder), Total = #sum{Price, B : winning_bid(B), bid(B, Bidder, Price)}.
% Then enforce budget constraint
:- total_spent(Bidder, Spent), budget(Bidder, Budget), Spent > Budget.

% 3. Licensing Requirement: To win bids with electronics/furniture items, must win corresponding license
% Helper: bidder wins electronics items
bidder_wins_electronics(Bidder) :- winning_bid(B), bid(B, Bidder, _), bid_items(B, I), category(I, electronics).
% Helper: bidder wins furniture items
bidder_wins_furniture(Bidder) :- winning_bid(B), bid(B, Bidder, _), bid_items(B, I), category(I, furniture).
% Helper: bidder wins electronics license
bidder_wins_lic_E(Bidder) :- winning_bid(B), bid(B, Bidder, _), bid_items(B, lic_E).
% Helper: bidder wins furniture license
bidder_wins_lic_F(Bidder) :- winning_bid(B), bid(B, Bidder, _), bid_items(B, lic_F).

% Licensing constraints
:- bidder_wins_electronics(Bidder), not bidder_wins_lic_E(Bidder).
:- bidder_wins_furniture(Bidder), not bidder_wins_lic_F(Bidder).

% 4. Fairness Constraint: Max 3 items per bidder
% Count items per bidder
items_per_bidder(Bidder, Count) :- bidder(Bidder), Count = #count{I, B : winning_bid(B), bid(B, Bidder, _), bid_items(B, I)}.
:- items_per_bidder(Bidder, Count), Count > 3.

% ==================== OBJECTIVE: MAXIMIZE REVENUE ====================
% Base revenue from winning bids
base_revenue(Base) :- Base = #sum{Price, B : winning_bid(B), bid(B, _, Price)}.

% Synergy bonus: if bidder wins 2 or more bids
bidder_wins_multiple(Bidder) :- winning_bid(B), bid(B, Bidder, _), #count{B : winning_bid(B), bid(B, Bidder, _)} >= 2.
synergy_revenue(Synergy) :- Synergy = #sum{Bonus, Bidder : bidder_wins_multiple(Bidder), synergy_bonus(Bidder, Bonus)}.

% Total revenue
total_revenue(Total) :- total_revenue = Base + Synergy, base_revenue(Base), synergy_revenue(Synergy).

% Maximize total revenue
#maximize { Total@1 : total_revenue(Total) }.

% ==================== OUTPUT ====================
% Show winning bids
#show winning_bid/1.

% Show total revenue
#show total_revenue/1.

% Show synergy bonuses received
#show bidder_wins_multiple/1.

% Show item allocation (item -> winning bidder)
item_allocated(I, Bidder) :- winning_bid(B), bid(B, Bidder, _), bid_items(B, I).
#show item_allocated/2.

% Show per-bidder spending
#show total_spent/2.