# Benchmark Report (SYSTEM1): ASPBench - 12_zebra_puzzle_easy

**Provider:** xiaomi2
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: high
**Duration:** 88.69s


 SYSTEM 1 PURE REASONING AGENT

 Query: # Problem Statement

The Zebra Puzzle, also known as Einstein's Riddle, is a classic logic puzzle. Five houses stand in a row, each painted a different color and inhabited by people of different nationalities who prefer different drinks, smoke different cigarettes, and keep different pets. The question is: who owns the zebra?

## Instance Data

There are **5 houses** in a row, numbered 1 to 5 from left to right. Each house has **exactly one** of each of the following attributes:
- **Color**: Red, Green, White, Yellow, Blue
- **Nationality**: Brit, Swede, Dane, Norwegian, German
- **Drink**: Tea, Coffee, Milk, Beer, Water
- **Cigarette**: Pall Mall, Dunhill, Blends, Blue Master, Prince
- **Pet**: Dog, Birds, Cats, Horse, Zebra

## Constraints

1. The Brit lives in the red house
2. The Swede keeps dogs as pets
3. The Dane drinks tea
4. The green house is on the **left** of the white house (directly adjacent)
5. The green house's owner drinks coffee
6. The person who smokes Pall Mall rears birds
7. The owner of the yellow house smokes Dunhill
8. The person living in the **center house** (house 3) drinks milk
9. The Norwegian lives in the **first house** (house 1)
10. The person who smokes Blends lives **next to** the one who keeps cats
11. The person who keeps a horse lives **next to** the person who smokes Dunhill
12. The owner who smokes Blue Master drinks beer
13. The German smokes Prince
14. The Norwegian lives **next to** the blue house
15. The person who smokes Blends has a neighbor who drinks water

## Objective

Find the complete assignment of attributes to houses that satisfies **all** constraints, and determine who owns the zebra.

## Output Format

Your solution must output a JSON object with the following structure:

```json
{
  "solution": [
    {
      "house": 1,
      "color": "Yellow",
      "nationality": "Norwegian",
      "drink": "Water",
      "cigarette": "Dunhill",
      "pet": "Cats"
    },
    ...
  ],
  "zebra_owner": "German"
}
```

- **solution**: Array of 5 objects (one per house, ordered 1-5), each containing:
  - **house**: House number (1-5)
  - **color**: Color of the house
  - **nationality**: Nationality of the resident
  - **drink**: Beverage preference
  - **cigarette**: Cigarette brand smoked
  - **pet**: Pet owned
- **zebra_owner**: Nationality of the person who owns the zebra


Return your final answer in JSON format.


### Thinking

- We are given the classic Zebra puzzle with 5 houses, each with attributes: color, nationality, drink, cigarette, pet. We need to find the assignment that satisfies all constraints. We'll solve step by step.
- Let's list constraints:
- 1. Brit lives in red house. 2. Swede keeps dogs. 3. Dane drinks tea. 4. Green house is left of white house (directly adjacent). So green house number = white house number - 1. 5. Green house's owner drinks coffee. 6. Pall Mall smoker rears birds. 7. Yellow house owner smokes Dunhill. 8. Center house (house 3) drinks milk. 9. Norwegian lives in first house (house 1). 10. Blends smoker lives next to cat owner. 11. Horse owner lives next to Dunhill smoker. 12. Blue Master smoker drinks beer. 13. German smokes Prince. 14. Norwegian lives next to blue house. 15. Blends smoker has a neighbor who drinks water.
- We need to assign each house a color, nationality, drink, cigarette, pet.
- We'll use logical deduction.
- Start with fixed positions:
- From 9: Norwegian in house 1. From 8: House 3 drinks milk. From 4: Green house left of white house, so possible pairs: (1,2), (2,3), (3,4), (4,5). But house 1 is Norwegian, so color of house 1 is not necessarily green or white? We'll see.
- From 14: Norwegian lives next to blue house. Since Norwegian is in house 1, next to house 1 is house 2. So house 2 must be blue. (Because only house 2 is adjacent to house 1). So house 2 color = Blue.
- Now we have house 2 = Blue.
- From 4: Green left of white. So green and white are adjacent. Possible pairs: (1,2), (2,3), (3,4), (4,5). But house 2 is blue, so (1,2) would mean house 1 green, house 2 white, but house 2 is blue, so not possible. (2,3) would mean house 2 green, house 3 white, but house 2 is blue, so not possible. So possible pairs: (3,4) or (4,5). So either green=3, white=4, or green=4, white=5.
- From 5: Green house's owner drinks coffee. So if green=3, then house 3 drinks coffee. But from 8, house 3 drinks milk. Contradiction. So green cannot be 3. Therefore green=4, white=5. So house 4 is green, house 5 is white.
- Now we have colors: house 1: ? (not blue, not green, not white), house 2: Blue, house 3: ? (not blue, not green, not white), house 4: Green, house 5: White. Remaining colors: Red, Yellow. So house 1 and house 3 are Red and Yellow in some order.
- From 1: Brit lives in red house. So red house is either house 1 or house 3. But house 1 is Norwegian, so if red house is house 1, then Brit would be Norwegian, contradiction. So red house cannot be house 1. Therefore red house is house 3. So house 3 is Red. Then house 1 must be Yellow.
- So colors: house 1: Yellow, house 2: Blue, house 3: Red, house 4: Green, house 5: White.
- From 7: Yellow house owner smokes Dunhill. So house 1 (Yellow) smokes Dunhill.
- From 5: Green house's owner drinks coffee. So house 4 (Green) drinks coffee.
- From 8: House 3 drinks milk.
- From 1: Brit lives in red house. So house 3 (Red) is Brit.
- From 9: Norwegian in house 1.
- Now nationalities: house 1: Norwegian, house 3: Brit. Remaining: Swede, Dane, German.
- From 3: Dane drinks tea. So Dane's drink is tea. We have drinks assigned: house 1: ?, house 2: ?, house 3: milk, house 4: coffee, house 5: ?. So tea must be in house 2 or house 5. So Dane is in house 2 or house 5.
- From 12: Blue Master smoker drinks beer. So whoever smokes Blue Master drinks beer.
- From 13: German smokes Prince.
- From 6: Pall Mall smoker rears birds.
- From 2: Swede keeps dogs.
- From 10: Blends smoker lives next to cat owner. From 11: Horse owner lives next to Dunhill smoker. From 15: Blends smoker has a neighbor who drinks water.
- We also have cigarette assignments: house 1 smokes Dunhill. So Dunhill is in house 1.
- From 11: Horse owner lives next to Dunhill smoker. So horse owner is next to house 1. That means horse owner is in house 2 (since only house 2 is adjacent to house 1). So house 2 has horse.
- So pet: house 2: Horse.
- Now from 10: Blends smoker lives next to cat owner. So Blends and cat are adjacent.
- From 15: Blends smoker has a neighbor who drinks water. So Blends smoker is next to someone who drinks water.
- We have drinks: house 3: milk, house 4: coffee. So water must be in house 1, 2, or 5. But house 1 smokes Dunhill, so not necessarily. We'll see.
- Now let's list what we know so far:
- House 1: Color: Yellow, Nationality: Norwegian, Drink: ?, Cigarette: Dunhill, Pet: ? House 2: Color: Blue, Nationality: ?, Drink: ?, Cigarette: ?, Pet: Horse House 3: Color: Red, Nationality: Brit, Drink: Milk, Cigarette: ?, Pet: ? House 4: Color: Green, Nationality: ?, Drink: Coffee, Cigarette: ?, Pet: ? House 5: Color: White, Nationality: ?, Drink: ?, Cigarette: ?, Pet: ?
- Remaining nationalities: Swede, Dane, German. Remaining drinks: Tea, Beer, Water (since milk and coffee taken). Remaining cigarettes: Pall Mall, Blends, Blue Master, Prince (Dunhill taken). Remaining pets: Dog, Birds, Cats, Zebra (Horse taken).
- From 3: Dane drinks tea. So Dane is in a house that drinks tea. Tea is not yet assigned. So Dane is in house 2 or house 5 (since house 1,3,4 drinks are unknown but house 1 could be tea? Actually house 1 drink not assigned, but Dane drinks tea, so if Dane is in house 1, then house 1 drinks tea. But house 1 is Norwegian, so Dane cannot be in house 1. So Dane is in house 2 or house 5. So either house 2 drinks tea and is Dane, or house 5 drinks tea and is Dane.
- From 12: Blue Master smoker drinks beer. So whoever smokes Blue Master, their drink is beer. Beer is not yet assigned. So Blue Master smoker is in a house that drinks beer.
- From 13: German smokes Prince. So German's cigarette is Prince.
- From 6: Pall Mall smoker rears birds. So Pall Mall and birds go together.
- From 2: Swede keeps dogs. So Swede's pet is dog.
- Now let's consider constraints about adjacency.
- We have Blends smoker next to cat owner. Also Blends smoker next to water drinker.
- We have horse owner in house 2, next to Dunhill smoker (house 1). That's satisfied.
- Now, let's try to assign nationalities to houses 2,4,5.
- House 2: Nationality could be Swede, Dane, or German. But Dane drinks tea, so if house 2 is Dane, then house 2 drinks tea. If house 2 is not Dane, then house 2's drink is something else.
- House 4: Nationality could be Swede, Dane, or German. But house 4 drinks coffee, so if Dane is in house 4, then Dane would drink coffee, but Dane drinks tea, so Dane cannot be in house 4. So house 4 is not Dane. So Dane is either house 2 or house 5.
- House 5: Nationality could be Swede, Dane, or German. If Dane is in house 5, then house 5 drinks tea.
- So possibilities: Dane in house 2 or house 5.
- Now consider German smokes Prince. So German's cigarette is Prince. Where can German be? Possibly house 2,4,5. But house 4 drinks coffee, and German could be there. House 2 and house 5 also possible.
- Now consider Swede keeps dogs. So Swede's pet is dog. Where can Swede be? Possibly house 2,4,5. But house 2 already has horse, so if Swede is in house 2, then pet would be dog, but house 2 has horse, contradiction. So Swede cannot be in house 2. So Swede is in house 4 or house 5.
- So nationalities: house 2: either Dane or German (since Swede excluded). House 4: either Swede or German. House 5: either Swede or Dane (since German could be elsewhere, but if German is in house 2 or 4, then house 5 could be Swede or Dane). But we also have Dane only in house 2 or 5. So if Dane is in house 2, then house 5 cannot be Dane, so house 5 would be Swede. If Dane is in house 5, then house 2 cannot be Dane, so house 2 would be German. And then house 4 would be Swede (since Swede must be in 4 or 5, and if house 5 is Dane, then Swede must be in house 4). So two scenarios:
- Scenario A: Dane in house 2, then house 2: Dane, house 4: Swede or German? But Swede must be in 4 or 5, and if Dane in 2, then house 5 could be Swede or German? But we also have German somewhere. Let's systematically list.
- We have three nationalities for houses 2,4,5: Swede, Dane, German. Constraints: Dane drinks tea, so Dane's house must have tea. Swede keeps dogs, so Swede's house must have dog. German smokes Prince.
- Also, house 2 has horse, so if Swede were in house 2, pet would be dog, but it's horse, so Swede not in house 2. So house 2 is either Dane or German. House 4 drinks coffee, so Dane cannot be in house 4 (since Dane drinks tea). So house 4 is either Swede or German. House 5: can be any, but if Dane is in house 5, then house 5 drinks tea.
- Now consider the two cases for Dane.
- Case 1: Dane in house 2. Then house 2: Dane, drink: tea (since Dane drinks tea). So house 2 drinks tea. Then remaining nationalities for houses 4 and 5: Swede and German. House 4: either Swede or German. House 5: the other. But Swede keeps dogs, so if Swede is in house 4, then house 4 pet is dog. If Swede is in house 5, then house 5 pet is dog. German smokes Prince, so if German is in house 4, then house 4 cigarette is Prince. If German is in house 5, then house 5 cigarette is Prince.
- Case 2: Dane in house 5. Then house 5: Dane, drink: tea. Then remaining nationalities for houses 2 and 4: Swede and German. But house 2 cannot be Swede (since house 2 has horse, not dog), so house 2 must be German. Then house 4 must be Swede. So in Case 2: house 2: German, house 4: Swede, house 5: Dane. Then house 2: German smokes Prince (from 13). So house 2 cigarette = Prince. House 4: Swede keeps dogs, so house 4 pet = dog. House 5: Dane drinks tea, so house 5 drink = tea.
- Now we need to see which case is consistent with other constraints.
- Let's also consider drinks: We have assigned: house 3: milk, house 4: coffee. In Case 1: house 2: tea. Then remaining drinks for house 1 and house 5: beer and water. In Case 2: house 5: tea, then remaining drinks for house 1 and house 2: beer and water.
- Now consider cigarettes: We have house 1: Dunhill. In Case 1: house 2: Dane, cigarette unknown (not necessarily Prince, because German is not in house 2). In Case 2: house 2: German, so cigarette = Prince. We also have Pall Mall, Blends, Blue Master, Prince to assign to houses 2,3,4,5 (house 1 has Dunhill). In Case 2, house 2 has Prince, so remaining: Pall Mall, Blends, Blue Master for houses 3,4,5. In Case 1, house 2 does not have Prince (unless German is in house 2, but in Case 1, house 2 is Dane, so not German, so house 2 does not have Prince). So Prince must be in house 4 or 5 (since German is in one of them). So in Case 1, Prince is in house 4 or 5.
- Now consider constraint 6: Pall Mall smoker rears birds. So Pall Mall and birds go together. Constraint 12: Blue Master smoker drinks beer. Constraint 13: German smokes Prince (already used). Constraint 10: Blends smoker next to cat owner. Constraint 15: Blends smoker next to water drinker.
- Also, we have pets: house 2: horse. In Case 1, if Swede is in house 4, then house 4 pet = dog; if Swede in house 5, then house 5 pet = dog. In Case 2, house 4 pet = dog.
- Now let's try to fill in more details.
- We also have constraint 14 already used (Norwegian next to blue house).
- Now, let's consider the adjacency for Blends. Blends smoker is next to cat owner and next to water drinker. So Blends smoker must have a neighbor who drinks water and a neighbor who has cats. Possibly the same neighbor or different? It says "lives next to the one who keeps cats" and "has a neighbor who drinks water". So at least one neighbor drinks water, and at least one neighbor keeps cats. They could be the same neighbor if that neighbor both drinks water and keeps cats, or different neighbors.
- Now, we know house 1 drinks either beer or water (in both cases). House 1 smokes Dunhill. So house 1 is not Blends. So Blends is in house 2,3,4, or 5.
- Also, water drinker is in house 1 or house 5 (in Case 1) or house 1 or house 2 (in Case 2). Actually, in Case 1: drinks: house 2 tea, house 3 milk, house 4 coffee, so remaining beer and water for house 1 and house 5. So water could be in house 1 or house 5. In Case 2: drinks: house 5 tea, house 3 milk, house 4 coffee, so remaining beer and water for house 1 and house 2. So water could be in house 1 or house 2.
- Now, Blends smoker must have a neighbor who drinks water. So if water is in house 1, then Blends must be in house 2 (since only house 2 is neighbor to house 1). If water is in house 5, then Blends must be in house 4 (neighbor to house 5). If water is in house 2, then Blends must be in house 1 or house 3. But house 1 smokes Dunhill, so not Blends, so if water in house 2, then Blends must be in house 3. So possibilities depend on water location.
- Also, Blends smoker must be next to cat owner. So wherever Blends is, there must be a cat in an adjacent house.
- Now, let's consider pets: We have horse in house 2. In Case 2, dog in house 4. In Case 1, dog in house 4 or 5. Also, birds will be with Pall Mall smoker. Cats and zebra are remaining.
- Now, let's examine Case 2 first because it seems more constrained.
- Case 2: Dane in house 5, German in house 2, Swede in house 4. So: House 1: Norwegian, Yellow, Dunhill, drink: ? (beer or water), pet: ? House 2: German, Blue, Prince, drink: ? (beer or water), pet: Horse House 3: Brit, Red, Milk, cigarette: ? (Pall Mall, Blends, or Blue Master), pet: ? House 4: Swede, Green, Coffee, cigarette: ? (Pall Mall, Blends, or Blue Master), pet: Dog House 5: Dane, White, Tea, cigarette: ? (Pall Mall, Blends, or Blue Master), pet: ?
- Remaining cigarettes: Pall Mall, Blends, Blue Master. Remaining pets: Birds, Cats, Zebra. Remaining drinks: Beer and Water for houses 1 and 2.
- Now, constraint 12: Blue Master smoker drinks beer. So whoever smokes Blue Master must have beer. So Blue Master cannot be in a house that drinks water. So Blue Master must be in a house that drinks beer. So if beer is in house 1, then Blue Master could be in house 1, but house 1 smokes Dunhill, so not. So Blue Master must be in house 2 if house 2 drinks beer, or in house 3,4,5 if they drink beer. But house 3 drinks milk, house 4 drinks coffee, house 5 drinks tea. So none of houses 3,4,5 drink beer. Therefore, the only house that can drink beer is house 1 or house 2. But house 1 smokes Dunhill, so cannot smoke Blue Master. So Blue Master must be in house 2, and house 2 must drink beer. Therefore, in Case 2, house 2 drinks beer, and house 2 smokes Blue Master? But wait, house 2 already smokes Prince (from German). So house 2 cannot smoke Blue Master. Contradiction. So Case 2 is impossible.
- Thus, Case 2 is ruled out.
- Therefore, we must have Case 1: Dane in house 2.
- So: House 2: Dane, Blue, drink: Tea (since Dane drinks tea), cigarette: ? (not Prince, because German is not in house 2), pet: Horse. House 4 and house 5: Swede and German in some order.
- Now, from earlier: Swede cannot be in house 2, so Swede is in house 4 or house 5. German is in the other.
- Now, we also have: German smokes Prince. So wherever German is, that house smokes Prince.
- Now, let's assign drinks: We have house 3: milk, house 4: coffee, house 2: tea. So remaining drinks: beer and water for houses 1 and 5.
- So house 1: either beer or water. House 5: either beer or water.
- Now, constraint 12: Blue Master smoker drinks beer. So Blue Master must be in a house that drinks beer. So Blue Master could be in house 1 (if house 1 drinks beer) or house 5 (if house 5 drinks beer) or possibly house 2,3,4 but house 2 drinks tea, house 3 milk, house 4 coffee, so only houses 1 and 5 can drink beer. So Blue Master must be in house 1 or house 5. But house 1 smokes Dunhill, so cannot smoke Blue Master. Therefore, Blue Master must be in house 5, and house 5 must drink beer. So house 5 drinks beer, and house 5 smokes Blue Master.
- Then house 1 must drink water.
- So we have: House 1: Norwegian, Yellow, Water, Dunhill, pet: ? House 5: ? (Swede or German), White, Beer, Blue Master, pet: ?
- Now, house 5 drinks beer and smokes Blue Master. That satisfies constraint 12.
- Now, remaining cigarettes: Pall Mall, Blends, Prince. Prince is for German. So German must be in a house that smokes Prince. German is either in house 4 or house 5. But house 5 smokes Blue Master, so German cannot be in house 5. Therefore, German must be in house 4. Then Swede must be in house 5.
- So: House 4: German, Green, Coffee, Prince, pet: ? House 5: Swede, White, Beer, Blue Master, pet: ?
- Now, Swede keeps dogs (constraint 2). So house 5 pet = Dog.
- Now, remaining pets: Birds, Cats, Zebra for houses 1,3,4? Actually house 4 pet not assigned yet, house 3 pet not assigned, house 1 pet not assigned. And we have birds, cats, zebra.
- Also, constraint 6: Pall Mall smoker rears birds. So Pall Mall and birds go together. Pall Mall is one of the remaining cigarettes? We have assigned: house 1: Dunhill, house 2: ?, house 3: ?, house 4: Prince, house 5: Blue Master. So remaining cigarettes: Pall Mall and Blends for houses 2 and 3. So Pall Mall must be in house 2 or house 3. And if Pall Mall is in a house, that house has birds.
- Now, constraint 10: Blends smoker lives next to cat owner. Constraint 15: Blends smoker has a neighbor who drinks water.
- We know house 1 drinks water. So Blends smoker must be next to house 1. That means Blends smoker must be in house 2 (since only house 2 is adjacent to house 1). So Blends is in house 2. Then house 2 smokes Blends.
- Then house 3 must smoke Pall Mall (since only Pall Mall left). So house 3 smokes Pall Mall, and therefore house 3 has birds (from constraint 6).
- Now, we have: House 2: Dane, Blue, Tea, Blends, Horse. House 3: Brit, Red, Milk, Pall Mall, Birds.
- Now, remaining pets: Cats and Zebra for houses 1 and 4. House 1: pet ? (Cats or Zebra) House 4: pet ? (Cats or Zebra)
- Now, constraint 10: Blends smoker (house 2) lives next to cat owner. So cat owner must be adjacent to house 2. Adjacent houses to house 2 are house 1 and house 3. House 3 has birds, so not cats. Therefore, cat owner must be in house 1. So house 1 has cats.
- Then house 4 must have zebra.
- So: House 1: Norwegian, Yellow, Water, Dunhill, Cats. House 4: German, Green, Coffee, Prince, Zebra.
- Now, check all constraints:
- 1. Brit in red house: House 3 is Brit and red. OK. 2. Swede keeps dogs: House 5 is Swede and has dog. OK. 3. Dane drinks tea: House 2 is Dane and drinks tea. OK. 4. Green house left of white: House 4 green, house 5 white, adjacent. OK. 5. Green house drinks coffee: House 4 green and drinks coffee. OK. 6. Pall Mall rears birds: House 3 smokes Pall Mall and has birds. OK. 7. Yellow house smokes Dunhill: House 1 yellow and smokes Dunhill. OK. 8. Center house drinks milk: House 3 drinks milk. OK. 9. Norwegian in first house: House 1 Norwegian. OK. 10. Blends next to cats: House 2 smokes Blends, house 1 has cats, adjacent. OK. 11. Horse next to Dunhill: House 2 has horse, house 1 smokes Dunhill, adjacent. OK. 12. Blue Master drinks beer: House 5 smokes Blue Master and drinks beer. OK. 13. German smokes Prince: House 4 German and smokes Prince. OK. 14. Norwegian next to blue house: House 1 Norwegian, house 2 blue, adjacent. OK. 15. Blends has neighbor who drinks water: House 2 smokes Blends, house 1 drinks water, adjacent. OK.
- All constraints satisfied.
- Thus, the zebra owner is German (house 4).
- Now, output JSON.
- We need to list houses 1 to 5 in order.
- House 1: house:1, color:"Yellow", nationality:"Norwegian", drink:"Water", cigarette:"Dunhill", pet:"Cats" House 2: house:2, color:"Blue", nationality:"Dane", drink:"Tea", cigarette:"Blends", pet:"Horse" House 3: house:3, color:"Red", nationality:"Brit", drink:"Milk", cigarette:"Pall Mall", pet:"Birds" House 4: house:4, color:"Green", nationality:"German", drink:"Coffee", cigarette:"Prince", pet:"Zebra" House 5: house:5, color:"White", nationality:"Swede", drink:"Beer", cigarette:"Blue Master", pet:"Dog"
- Zebra owner: "German"
- Now, write JSON.


```json
{
  "solution": [
    {
      "house": 1,
      "color": "Yellow",
      "nationality": "Norwegian",
      "drink": "Water",
      "cigarette": "Dunhill",
      "pet": "Cats"
    },
    {
      "house": 2,
      "color": "Blue",
      "nationality": "Dane",
      "drink": "Tea",
      "cigarette": "Blends",
      "pet": "Horse"
    },
    {
      "house": 3,
      "color": "Red",
      "nationality": "Brit",
      "drink": "Milk",
      "cigarette": "Pall Mall",
      "pet": "Birds"
    },
    {
      "house": 4,
      "color": "Green",
      "nationality": "German",
      "drink": "Coffee",
      "cigarette": "Prince",
      "pet": "Zebra"
    },
    {
      "house": 5,
      "color": "White",
      "nationality": "Swede",
      "drink": "Beer",
      "cigarette": "Blue Master",
      "pet": "Dog"
    }
  ],
  "zebra_owner": "German"
}
```

### TOKEN USAGE

  Input tokens:  689
  Output tokens: 5,998
  Total tokens:  6,687

COMPLETE

## System 1 Final Answer

```json
```json
{
  "solution": [
    {
      "house": 1,
      "color": "Yellow",
      "nationality": "Norwegian",
      "drink": "Water",
      "cigarette": "Dunhill",
      "pet": "Cats"
    },
    {
      "house": 2,
      "color": "Blue",
      "nationality": "Dane",
      "drink": "Tea",
      "cigarette": "Blends",
      "pet": "Horse"
    },
    {
      "house": 3,
      "color": "Red",
      "nationality": "Brit",
      "drink": "Milk",
      "cigarette": "Pall Mall",
      "pet": "Birds"
    },
    {
      "house": 4,
      "color": "Green",
      "nationality": "German",
      "drink": "Coffee",
      "cigarette": "Prince",
      "pet": "Zebra"
    },
    {
      "house": 5,
      "color": "White",
      "nationality": "Swede",
      "drink": "Beer",
      "cigarette": "Blue Master",
      "pet": "Dog"
    }
  ],
  "zebra_owner": "German"
}
```
```
