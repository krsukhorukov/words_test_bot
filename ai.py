from imports import *

def compare(word, user_input):
    # client = OpenAI(api_key=API_KEY)

    # system_prompt = """
    # Ты — эксперт по сравнению значений слов и фраз. Тебе даны две строки: первая из словаря, вторая — введённая пользователем (может содержать ошибки, пропуск букв, быть производной формой, синонимом и т.п.).

    #     1. Определи, совпадают ли они по смыслу (включая близость значений, орфографические и стилистические опечатки).
    #     2. Если считаешь, что они совпадают, выведи «1». Если нет — выведи «0».
    #     3. Ответ должен содержать только одну цифру («0» или «1») без пробелов, точек, других символов или пояснений.

    # Важно: ответь максимально точно и честно. Если ты не уверен, лучше выбери вариант, что они не совпадают. Однако, сравнение не должно быть строгим, учти, что пользователь может допустить опечатки или использовать синонимы.
    # """

    # user_prompt = f"Слово из словаря: \"{word}\", введённое пользователем: \"{user_input}\""

    # try:
    #     response = client.chat.completions.create(
    #         messages=[
    #             {"role": "system", "content": system_prompt},
    #             {"role": "user", "content": user_prompt}
    #         ],
    #         max_tokens=10,
    #         temperature=0,
    #         n=1,
    #         stop=None,
    #         model="gpt-4o-mini",
    #     )
    #     output = response.choices[0].message.content
    #     print(output)
    #     return int(output)
    # except Exception as e:
    #     logger.error(f"Ошибка при сравнении текста: {e}")
    #     return 0

    return 