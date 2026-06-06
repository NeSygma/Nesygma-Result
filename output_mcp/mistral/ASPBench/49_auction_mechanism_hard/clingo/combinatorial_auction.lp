% --- Facts ---
% Bidders: id, budget, synergy_bonus
bidder(a, 150, 20).
bidder(b, 200, 10).
bidder(c, 180, 25).
bidder(d, 100, 5).

% Items: id, category (electronics, furniture, or license)
item(item1, electronics).
item(item2, electronics).
item(item3, furniture).
item(item4, furniture).
item(item5, electronics).
item(item6, furniture).
item(lic_E, license_electronics).
item(lic_F, license_furniture).

% Bids: id, bidder, price
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

% Bid items: bid_id, item
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

% Category to license mapping
category_license(electronics, lic_E).
category_license(furniture, lic_F).

% --- Choice Rules ---
% A bid can be selected as winning or not
{ winning_bid(BidID) } :- bid(BidID, _, _).

% If a bid wins, allocate its items to the bidder
allocated_item(Item, Bidder) :- winning_bid(BidID), bid(BidID, Bidder, _), bid_item(BidID, Item).

% --- Constraints ---

% 1. Item exclusivity: Each item can be allocated to at most one bidder
:- allocated_item(Item, Bidder1), allocated_item(Item, Bidder2), Bidder1 != Bidder2.

% 2. Budget compliance: Total price of winning bids for a bidder cannot exceed their budget
% Helper: sum of prices for winning bids per bidder
% We use a constraint to ensure the sum of prices does not exceed the budget
:- bidder(Bidder, Budget, _),
    TotalPrice = #sum[BidPrice : winning_bid(BidID), bid(BidID, Bidder, BidPrice)],
    TotalPrice > Budget.

% 3. Synergy bonus: If a bidder wins 2+ bids, add their synergy bonus to revenue
% Helper: count of winning bids per bidder
winning_bid_count(Bidder, Count) :- bidder(Bidder, _, _),
    Count = #count[BidID : winning_bid(BidID), bid(BidID, Bidder, _)].
% Synergy bonus applied if count >= 2
synergy_bonus_applied(Bidder) :- winning_bid_count(Bidder, Count), Count >= 2.

% 4. Licensing requirement: If a bidder wins a bid containing items from category C,
% they must also win the license bid for category C
% Helper: categories present in winning bids for a bidder
winning_bid_category(Bidder, Category) :- winning_bid(BidID), bid(BidID, Bidder, _),
    bid_item(BidID, Item), item(Item, Category).
% Helper: license bids for categories
license_bid_for_category(Category, LicenseItem) :- category_license(Category, LicenseItem).
% Constraint: if a category is present, the corresponding license must be won
:- winning_bid_category(Bidder, Category),
    license_bid_for_category(Category, LicenseItem),
    not winning_bid(LicenseBidID),
    bid(LicenseBidID, Bidder, _), bid_item(LicenseBidID, LicenseItem).

% 5. Fairness constraint: No bidder can be allocated more than 3 items
% Helper: count of allocated items per bidder
allocated_item_count(Bidder, Count) :- bidder(Bidder, _, _),
    Count = #count[Item : allocated_item(Item, Bidder)].
:- allocated_item_count(Bidder, Count), Count > 3.

% --- Revenue calculation ---
% Total revenue = sum of winning bid prices + sum of synergy bonuses for applicable bidders
% We use #sum in the optimization statement to maximize revenue

% --- Optimization ---
% Maximize total revenue: sum of winning bid prices + sum of synergy bonuses
#maximize { Revenue : 
    Revenue = #sum[BidPrice : winning_bid(BidID), bid(BidID, _, BidPrice)]
    + #sum[Bonus : synergy_bonus_applied(Bidder), bidder(Bidder, _, Bonus)]
}.

% --- Show directives ---
#show winning_bid/1.
#show total_revenue/1.
#show allocated_item/2.
#show synergy_bonus_applied/1.