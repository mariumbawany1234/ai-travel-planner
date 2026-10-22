"""Prompt builders for the three prompting techniques."""
from dataclasses import dataclass
from typing import List


@dataclass
class Traveler:
    name: str
    destination: str
    days: int
    budget: float
    interests: List[str]
    travel_style: str  # Solo / Family / Friends

    def summary(self) -> str:
        return (
            f"- Name: {self.name}\n"
            f"- Destination: {self.destination}\n"
            f"- Days: {self.days}\n"
            f"- Budget: ${self.budget:,.0f} (total, per trip)\n"
            f"- Interests: {', '.join(self.interests)}\n"
            f"- Travel Style: {self.travel_style}"
        )


# --------------------------------------------------------------------------
# Part 1: Zero-Shot  (no examples, just the task)
# --------------------------------------------------------------------------
def build_zero_shot_prompt(t: Traveler) -> str:
    return f"""You are a travel planning assistant.

Here is the traveler's information:
{t.summary()}

Please:
1. Analyze the traveler's preferences.
2. Suggest places to visit in {t.destination}.
3. Create a day-by-day itinerary for {t.days} days.
4. Recommend activities that fit within the ${t.budget:,.0f} budget.

Include an estimated cost for each day and a short budget summary at the end."""


# --------------------------------------------------------------------------
# Part 2: Few-Shot  (2-3 example travelers + itineraries, then the new one)
# --------------------------------------------------------------------------
FEW_SHOT_EXAMPLES = """
### Example 1
Traveler:
- Name: Sara
- Destination: Istanbul
- Days: 3
- Budget: $500
- Interests: History, Food
- Travel Style: Solo

Itinerary:
**Profile:** Budget-conscious solo traveler who loves history and street food.
**Day 1 - Old City (~$150):**
- Morning: Hagia Sophia and Blue Mosque (~$30)
- Afternoon: Basilica Cistern + Grand Bazaar browsing (~$25)
- Evening: Street food dinner in Sultanahmet - simit, doner, baklava (~$15)
**Day 2 - Culture & Cuisine (~$170):**
- Morning: Topkapi Palace (~$35)
- Afternoon: Bosphorus ferry ride (~$5)
- Evening: Meyhane dinner in Karakoy (~$30)
**Day 3 - Local Life (~$130):**
- Morning: Spice Bazaar + Turkish breakfast (~$20)
- Afternoon: Galata Tower and walk through Beyoglu (~$20)
**Budget summary:** ~$450 of $500 (hostel + transport included).

### Example 2
Traveler:
- Name: The Khan Family
- Destination: Bali
- Days: 4
- Budget: $1200
- Interests: Nature, Beaches
- Travel Style: Family

Itinerary:
**Profile:** Family with kids who want relaxed nature and beach time.
**Day 1 - Arrival & Beach (~$250):**
- Morning: Check in at a family-friendly resort in Sanur
- Afternoon: Calm, shallow Sanur Beach (~$0)
- Evening: Seafood dinner on the beach (~$50)
**Day 2 - Nature Day (~$300):**
- Morning: Tegallalang Rice Terraces (~$10)
- Afternoon: Monkey Forest, Ubud (~$20)
- Evening: Family dinner in Ubud (~$40)
**Day 3 - Water Fun (~$300):**
- Morning: Snorkeling at Blue Lagoon (~$60)
- Afternoon: Beach club with pool (~$40)
**Day 4 - Culture & Farewell (~$200):**
- Morning: Tirta Empul water temple (~$15)
**Budget summary:** ~$1,050 of $1,200 (accommodation included).

### Example 3
Traveler:
- Name: Jake & Friends
- Destination: Cape Town
- Days: 3
- Budget: $700
- Interests: Adventure, Nature
- Travel Style: Friends

Itinerary:
**Profile:** Energetic group wanting outdoor adventure on a moderate budget.
**Day 1 - Table Mountain (~$200):**
- Morning: Hike Platteklip Gorge (free) or cable car (~$25)
- Afternoon: Camps Bay beach
- Evening: Braai-style group dinner (~$25 each)
**Day 2 - Peninsula Adventure (~$250):**
- Morning: Cape Point + Cape of Good Hope (~$20)
- Afternoon: Boulders Beach penguins (~$10)
- Evening: Sunset at Chapman's Peak
**Day 3 - Adrenaline (~$200):**
- Morning: Shark-cage diving or sandboarding (~$80)
- Afternoon: Kirstenbosch Gardens (~$10)
**Budget summary:** ~$650 of $700.
"""


def build_few_shot_prompt(t: Traveler) -> str:
    return f"""You are a travel planning assistant. Below are example travelers and the
itineraries that were created for them. Follow the same style, structure and level of
detail (profile line, day-by-day plan with estimated costs, budget summary).

{FEW_SHOT_EXAMPLES}

### Now your turn
Traveler:
{t.summary()}

Itinerary:"""


# --------------------------------------------------------------------------
# Part 3: Structured Reasoning (steps given, only short justifications asked)
# --------------------------------------------------------------------------
def build_structured_prompt(t: Traveler) -> str:
    return f"""You are an expert travel planner. Create a personalized travel plan for this traveler:
{t.summary()}

Work through these steps and present ONLY the final results of each step:
1. Analyze the traveler's preferences (interests and travel style).
2. Consider the available budget and how it should be split (stay, food, transport, activities).
3. Consider the number of travel days ({t.days}) and how to pace them.
4. Select suitable attractions and activities in {t.destination}.
5. Create a day-by-day itinerary with estimated daily costs.
6. Briefly explain why each recommendation was selected.

Output format (use these exact headings):
## 1. Traveler Profile
## 2. Budget Plan
## 3. Trip Pacing
## 4. Selected Attractions & Activities
## 5. Day-by-Day Itinerary
## 6. Why These Picks
(One short sentence of justification per recommendation.)

Rules:
- Do NOT reveal your internal reasoning or thought process.
- Give only short, clear justifications.
- Keep total estimated cost within ${t.budget:,.0f}."""


TECHNIQUES = {
    "Zero-Shot": build_zero_shot_prompt,
    "Few-Shot": build_few_shot_prompt,
    "Structured Reasoning": build_structured_prompt,
}
