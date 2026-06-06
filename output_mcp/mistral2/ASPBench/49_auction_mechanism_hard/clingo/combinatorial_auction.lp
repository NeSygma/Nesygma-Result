% --- DOMAINS ---
bidder(a; b; c; d).
item(item1; item2; item3; item4; item5; item6; lic_E; lic_F).
bid(1..10).
category(electronics; furniture).

% --- FACTS ---
% Bidder information: budget and synergy bonus
bidder(a, 150, 20).
bidder(b, 200, 10).
bidder(c, 180, 25).
bidder(d, 100, 5).

% Bid information: bidder, price, and items
bid(1, a, 70). bid_items(1, item1). bid_items(1, item2).
bid(2, a, 40). bid_items(2, lic_E).
bid(3, b, 90). bid_items(3, item3). bid_items(3, item4).
bid(4, b, 50). bid_items(4, lic_F).
bid(5, b, 60). bid_items(5, item5).
bid(6, c, 100). bid_items(6, item1). bid_items(6, item5).
bid(7, c, 60). bid_items(7, lic_E).
bid(8, c, 80). bid_items(8, item3). bid_items(8, item6).
bid(9, d, 25). bid_items(9, lic_F).
bid(10, d, 70). bid_items(10, item4).

% Item categories
item_category(item1, electronics). item_category(item2, electronics).
item_category(item5, electronics). item_category(lic_E, electronics).
item_category(item3, furniture). item_category(item4, furniture).
item_category(item6, furniture). item_category(lic_F, furniture).

% --- CHOICE RULE: Select winning bids ---
{ winning_bid(BidID) : bid(BidID, _, _) }.

% --- DERIVED PREDICATES ---
% Allocate items to winning bids
allocated_item(Item, BidID) :-
    winning_bid(BidID),
    bid_items(BidID, Item).

% Count number of winning bids per bidder
num_winning_bids(Bidder, N) :-
    bidder(Bidder, _, _),
    N = #count { BidID : winning_bid(BidID), bid(BidID, Bidder, _) }.

% Check if a bidder wins a license for a category
license_for(lic_E, electronics).
license_for(lic_F, furniture).

has_license(Bidder, Category) :-
    winning_bid(BidID),
    bid(BidID, Bidder, _),
    bid_items(BidID, Item),
    item_category(Item, Category),
    license_for(License, Category),
    winning_bid(LicenseBid),
    bid(LicenseBid, Bidder, _),
    bid_items(LicenseBid, License).

% --- CONSTRAINTS ---
% 1. Item Exclusivity: Each item can be allocated to at most one winning bid
:- allocated_item(Item, BidID1), allocated_item(Item, BidID2), BidID1 != BidID2.

% 2. Budget Compliance: Sum of prices of winning bids for a bidder ≤ their budget
:- winning_bid(BidID), bid(BidID, Bidder, Price),
   TotalPrice = #sum { P : winning_bid(B), bid(B, Bidder, P) },
   bidder(Bidder, BudgetMax, _),
   TotalPrice > BudgetMax.

% 3. Licensing Requirement: If a bidder wins a bid with items from a category,
%    they must also win the license bid for that category
:- winning_bid(BidID),
   bid(BidID, Bidder, _),
   bid_items(BidID, Item),
   item_category(Item, Category),
   not has_license(Bidder, Category).

% 4. Fairness Constraint: No bidder can be allocated more than 3 items
:- bidder(Bidder), #count { Item : allocated_item(Item, _) }, bidder_wins_item(Bidder, Item) } > 3.

bidder_wins_item(Bidder, Item) :-
    winning_bid(BidID),
    bid(BidID, Bidder, _),
    bid_items(BidID, Item).

% --- SYNERGY BONUS ---
% Add synergy bonus if a bidder wins ≥2 bids
synergy_bonus(Bidder, Bonus) :-
    num_winning_bids(Bidder, N),
    N >= 2,
    bidder(Bidder, _, Bonus).

% --- TOTAL REVENUE ---
% Calculate total revenue: sum of winning bid prices + synergy bonuses
revenue_from_bids(Revenue) :-
    Revenue = #sum { Price : bid(B, _, Price), winning_bid(B) }.

revenue_from_synergy(TotalBonus) :-
    TotalBonus = #sum { Bonus : synergy_bonus(Bidder, Bonus) }.

total_revenue(Revenue) :-
    revenue_from_bids(BidRevenue),
    revenue_from_synergy(SynergyRevenue),
    Revenue = BidRevenue + SynergyRevenue.

% --- OPTIMIZATION ---
#maximize { Revenue : total_revenue(Revenue) }.

% --- OUTPUT ---
#show winning_bid/1.
#show total_revenue/1.
#show synergy_bonus/2.
#show allocated_item/2.