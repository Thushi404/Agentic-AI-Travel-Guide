from tools.maps import search_places                                         # imports the search_places function from the maps module to find nearby attractions.
from tools.weather import get_weather                                        # imports the get_weather function from the weather module to get the weather forecast.


def create_itinerary(destination: str, days: int = 1, budget: str = "medium") -> dict:          # function creates a travel plan.
    days = max(1, min(days, 7))                                                                 # This ensures the itinerary is between 1 and 7 days.


    weather = get_weather(destination, "today")                                                 # Retrives today's weather for the destinantion.
    attractions = search_places(destination, "attractions", radius_m=8000, limit=days * 3)
    restaurants = search_places(destination, "restaurants", radius_m=8000, limit=days * 2)
    cafes = search_places(destination, "coffee shops", radius_m=8000, limit=days)

    attraction_list = attractions.get("results", [])
    restaurant_list = restaurants.get("results", [])
    cafe_list = cafes.get("results", [])

    plan = []                                                                                # this list will store the shedule for the each day.

    for day_number in range(1, days + 1):                                                          # loops through each day of the trip.
        first_index = (day_number - 1) * 3

        day_attractions = attraction_list[first_index:first_index + 3]
        lunch = restaurant_list[(day_number - 1) % len(restaurant_list)] if restaurant_list else None        # Uses the modulus operator % to rotate through restaurants.
        coffee = cafe_list[(day_number - 1) % len(cafe_list)] if cafe_list else None

        plan.append(                          # create's each day shedule and appends it to the plan list.
            {
                "day": day_number,
                "morning": day_attractions[0] if len(day_attractions) > 0 else "Explore city center",
                "lunch": lunch if lunch else "Find a local restaurant nearby",
                "afternoon": day_attractions[1] if len(day_attractions) > 1 else "Visit a museum or park", # fallback activity if there are not enough attractions.
                "evening": day_attractions[2] if len(day_attractions) > 2 else "Walk around a popular area",
                "coffee_break": coffee if coffee else "Optional cafe stop",
            }
        )

    return {                                                                                                  # return the final itinerary.
        "destination": destination,
        "days": days,
        "budget": budget,
        "weather_summary": weather,
        "itinerary": plan,
        "packing_tip": "Carry an umbrella or raincoat." if weather.get("umbrella_needed") else "Normal light travel packing is enough.",
    }
                  
    