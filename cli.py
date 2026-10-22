"""Command-line version.  Run:  python cli.py"""
from gemini_client import generate
from prompts import Traveler, TECHNIQUES


def main():
    print("=== AI Travel Planner (Gemini) ===")
    name = input("Name: ").strip()
    destination = input("Destination: ").strip()
    days = int(input("Number of days: "))
    budget = float(input("Budget (USD): "))
    interests = [i.strip() for i in input("Interests (comma separated): ").split(",") if i.strip()]
    style = input("Travel style (Solo/Family/Friends): ").strip()

    traveler = Traveler(name, destination, days, budget, interests, style)

    names = list(TECHNIQUES)
    print("\nChoose technique:")
    for i, n in enumerate(names, 1):
        print(f"  {i}. {n}")
    choice = names[int(input("Option (1-3): ")) - 1]

    text, secs = generate(TECHNIQUES[choice](traveler))
    print(f"\n--- {choice} result ({secs:.1f}s) ---\n")
    print(text)


if __name__ == "__main__":
    main()
