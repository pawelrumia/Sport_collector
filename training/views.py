from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Exercise
from .utils import ExerciseFactory
from django.shortcuts import render

@csrf_exempt
def add_exercise(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sport = data.get('sport')
            details = data.get('details', {})

            # Walidacja sportu
            if sport not in [choice[0] for choice in Exercise.SPORT_CHOICES]:
                return JsonResponse({"error": "Unsupported sport type"}, status=400)

            # Sprawdzenie wymaganych pól w details
            if sport == 'swimming':
                if 'time' not in details or 'pool_lengths' not in details:
                    return JsonResponse({"error": "Swimming requires 'time' and 'pool_lengths'"}, status=400)

            # Obliczenie spalonych kalorii
            calories_burned = ExerciseFactory.calculate_calories(sport, details)

            # Zapis ćwiczenia
            exercise = Exercise(sport=sport, details=details, calories_burned=calories_burned)
            exercise.save()

            return JsonResponse({
                "message": "Exercise added successfully!",
                "exercise": {
                    "id": exercise.id,
                    "sport": exercise.sport,
                    "details": exercise.details,
                    "calories_burned": exercise.calories_burned
                }
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred", "details": str(e)}, status=500)
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)

def get_exercises(request):
    if request.method == 'GET':
        try:
            exercises = Exercise.objects.all()
            result = [
                {
                    "id": exercise.id,
                    "date": exercise.date,
                    "sport": exercise.sport,
                    "details": exercise.details,
                    "calories_burned": exercise.calories_burned
                }
                for exercise in exercises
            ]
            return JsonResponse(result, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred", "details": str(e)}, status=500)
    return JsonResponse({"error": "Only GET method is allowed"}, status=405)

@csrf_exempt
def update_exercise_details(request, exercise_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            details = data.get('details', {})

            # Pobranie istniejącego ćwiczenia
            exercise = Exercise.objects.get(id=exercise_id)

            # Walidacja szczegółów dla danego sportu
            if exercise.sport == "running":
                if 'time' not in details or 'distance' not in details:
                    return JsonResponse({"error": "Running requires 'time' and 'distance'"}, status=400)
            elif exercise.sport == "swimming":
                if 'time' not in details or 'pool_lengths' not in details:
                    return JsonResponse({"error": "Swimming requires 'time' and 'pool_lengths'"}, status=400)
            elif exercise.sport == "pullups":
                if 'sets' not in details or 'reps_per_set' not in details:
                    return JsonResponse({"error": "Pull-ups require 'sets' and 'reps_per_set'"}, status=400)
            elif exercise.sport == "cycling":
                if 'time' not in details or 'distance' not in details:
                    return JsonResponse({"error": "Cycling requires 'time' and 'distance'"}, status=400)
            elif exercise.sport == "pushups":
                if 'sets' not in details or 'reps_per_set' not in details:
                    return JsonResponse({"error": "Push-ups require 'sets' and 'reps_per_set'"}, status=400)
            elif exercise.sport == "weights":
                if 'exercise_type' not in details or 'sets' not in details or 'reps_per_set' not in details:
                    return JsonResponse({"error": "Weights require 'exercise_type', 'sets', and 'reps_per_set'"}, status=400)

            # Aktualizacja pola details i przeliczenie kalorii
            exercise.details = details
            exercise.calories_burned = ExerciseFactory.calculate_calories(exercise.sport, details)
            exercise.save()

            return JsonResponse({
                "message": "Exercise details updated successfully!",
                "exercise": {
                    "id": exercise.id,
                    "sport": exercise.sport,
                    "details": exercise.details,
                    "calories_burned": exercise.calories_burned
                }
            }, status=200)

        except Exercise.DoesNotExist:
            return JsonResponse({"error": "Exercise not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred", "details": str(e)}, status=500)
    return JsonResponse({"error": "Only PUT method is allowed"}, status=405)


@csrf_exempt
def delete_exercise(request, exercise_id):
    """
    Deletes an exercise record by its ID.
    """
    if request.method == 'DELETE':
        try:
            # Find the exercise by ID
            exercise = Exercise.objects.get(id=exercise_id)

            # Delete the exercise
            exercise.delete()

            return JsonResponse({
                "message": f"Exercise with ID {exercise_id} deleted successfully!"
            }, status=200)
        except Exercise.DoesNotExist:
            return JsonResponse({
                "error": f"Exercise with ID {exercise_id} does not exist"
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "error": "An unexpected error occurred",
                "details": str(e)
            }, status=500)
    else:
        return JsonResponse({"error": "Only DELETE method is allowed"}, status=405)


def exercise_form(request):
    if request.method == 'POST':
        try:
            sport = request.POST.get('sport')
            details = {}

            # Pobieranie odpowiednich danych z formularza
            if sport == 'running':
                details['time'] = request.POST.get('time')
                details['distance'] = request.POST.get('distance')
            elif sport == 'swimming':
                details['time'] = request.POST.get('time')
                details['pool_lengths'] = request.POST.get('pool_lengths')
            elif sport == 'pullups':
                details['sets'] = request.POST.get('sets')
                details['reps_per_set'] = request.POST.get('reps_per_set')
            elif sport == 'cycling':
                details['time'] = request.POST.get('time')
                details['distance'] = request.POST.get('distance')
            elif sport == 'pushups':
                details['sets'] = request.POST.get('sets')
                details['reps_per_set'] = request.POST.get('reps_per_set')
            elif sport == 'weights':
                details['exercise_type'] = request.POST.get('exercise_type')
                details['sets'] = request.POST.get('sets')
                details['reps_per_set'] = request.POST.get('reps_per_set')

            # Tworzenie ćwiczenia
            exercise = Exercise(sport=sport, details=details)
            exercise.save()

            return JsonResponse({"message": "Exercise added successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, 'training/exercise_form.html')