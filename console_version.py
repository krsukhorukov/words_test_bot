import random
from termcolor import colored
from vocabulary import *

def choose_translation_direction():
    print("Выберите направление перевода:")
    print("1. С французского на русский")
    print("2. С русского на французский")

    choice = input("Введите номер выбранного направления (1 или 2): ")
    return choice == '1'

def run_my_vocabulary_quiz(my_vocabulary, from_english_to_russian):
    results = []
    correct_count = 0
    total_count = 0

    for word, translations in my_vocabulary.items():
        if from_english_to_russian:
            print("Слово:", word)
            user_translation = input("Ваш перевод: ").strip().lower()
            correct_translations = [translation.strip().lower() for translation in translations.split(',')]
        else:
            print("Перевод:", translations)
            user_translation = input("Введите слово на английском: ").strip().lower()
            correct_translations = [translation.strip().lower() for translation in translations.split(',')]

        if user_translation == '0':
            break

        total_count += 1

        if user_translation in correct_translations:
            correct_count += 1
            results.append((word, user_translation, ', '.join(correct_translations), True))
        else:
            results.append((word, user_translation, ', '.join(correct_translations), False))

    return results, correct_count, total_count

def display_results(results, correct_count, total_count):
    for word, user_translation, correct_translations, is_correct in results:
        if is_correct:
            print(colored(f"{word}: {user_translation} (Правильно)", 'green'))
        elif not correct_translations:
            print(colored(f"{word}: {user_translation} (Нет перевода)", 'blue'))
        else:
            print(colored(f"{word}: {user_translation} (Неправильно, {correct_translations})", 'red'))

    percentage = (correct_count / total_count) * 100 if total_count > 0 else 0
    print(f"\nПроцент правильных ответов: {percentage:.2f}%")
    print(f"Статистика: {correct_count}/{total_count} правильных ответов")

def main():
    my_vocabulary = vocabulary
    
    print("Добро пожаловать в программу по изучению слов!")

    from_english_to_russian = choose_translation_direction()

    print("Введите перевод слова. Введите '0' для завершения.")

    random.seed()  # Инициализация генератора случайных чисел
    shuffled_keys = list(my_vocabulary.keys())
    random.shuffle(shuffled_keys)

    results, correct_count, total_count = run_my_vocabulary_quiz({key: my_vocabulary[key] for key in shuffled_keys}, from_english_to_russian)
    display_results(results, correct_count, total_count)

if __name__ == "__main__":
    main()
