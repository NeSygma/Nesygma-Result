at(1, restaurant).
at(2, optometrist).
at(3, toy_store).
at(4, restaurant).
at(5, shoe_store).
at(6, veterinarian).
at(7, pharmacy).

option(e) :- 
    at(1, restaurant), 
    at(2, optometrist), 
    at(3, toy_store), 
    at(4, restaurant), 
    at(5, shoe_store), 
    at(6, veterinarian), 
    at(7, pharmacy).

#show option/1.