class ExerciseFactory:
    @staticmethod
    def calculate_calories(sport, details):
        if sport == 'running' or sport == 'cycling':
            # Dla biegania i jazdy na rowerze: kalorie = czas (w minutach) * współczynnik
            time = details.get('time', 0)
            return time * 10  # Przykładowy współczynnik: 10 kalorii na minutę
        elif sport == 'swimming':
            # Dla pływania: kalorie = czas (w minutach) * współczynnik
            time = details.get('time', 0)
            return time * 12  # Przykładowy współczynnik: 12 kalorii na minutę
        elif sport == 'pullups' or sport == 'pushups':
            # Dla podciągnięć i pompek: kalorie = liczba powtórzeń * współczynnik
            sets = details.get('sets', 0)
            reps_per_set = details.get('reps_per_set', 0)
            total_reps = sets * reps_per_set
            return total_reps * 0.5  # Przykładowy współczynnik: 0.5 kalorii na powtórzenie
        elif sport == 'weights':
            # Dla ćwiczeń z hantlami: kalorie = liczba powtórzeń * współczynnik
            sets = details.get('sets', 0)
            reps_per_set = details.get('reps_per_set', 0)
            return sets * reps_per_set * 0.6  # Przykładowy współczynnik: 0.6 kalorii na powtórzenie
        else:
            return 0  # Wartość domyślna dla nieobsługiwanych sportów
