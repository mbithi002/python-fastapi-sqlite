# # Personal information form

# name = input("Enter your name: ")
# age = input("Enter your age: ")
# city = input("Enter your city: ")
# hobby = input("Enter your hobby: ")

# print(f"Hello, my name is {name}. I am {age} years old, I live in {city}, and I love {hobby}.")

# # calculator
# num1 = float(input("Enter the first number: "))
# num2 = float(input("Enter the second number: "))
# operation = input("Choose an operation (+, -, *, /): ")

# if operation == '+':
#     result = num1 + num2
# elif operation == '-':
#     result = num1 - num2
# elif operation == '*':
#     result = num1 * num2
# elif operation == '/':
#     if num2 == 0:
#         result = "Error: Division by zero"
#     else:
#         result = num1 / num2
# else:
#     result = "Error: Invalid operation"

# print(result)

# # number guessing game
import random

number = random.randint(1, 100)
# print(f"Computer generated number {number}")                                                                                                                                                                                                                                                                                                                                                                                           
attempts = 0

while True:
    guess = int(input("Guess the number (1-100): "))
    attempts += 1
    if guess < number:
        print("Too low")
    elif guess > number:
        print("Too high")
    else:
        print(f"Correct! You guessed it in {attempts} attempts.")
        break

# string manipulation
sentence = input("Enter a sentence: ")

print(sentence.upper())
print(sentence.lower())
print(f"Number of words: {len(sentence.split())}")
print(sentence[::-1])
words = sentence.split()
print(f"First word: {words[0]}")
print(f"Last word: {words[-1]}")


# Temperature converter
while True:
    temp = float(input("Enter the temperature: "))
    unit = input("Enter the unit (C or F): ").upper()

    if unit == 'C':
        converted = (temp * 9/5) + 32
        print(f"{temp}°C is {converted}°F")
    elif unit == 'F':
        converted = (temp - 32) * 5/9
        print(f"{temp}°F is {converted}°C")
    else:
        print("Invalid unit")

    again = input("Do you want to convert another temperature? (yes/no): ").lower()
    if again != 'yes':
        break