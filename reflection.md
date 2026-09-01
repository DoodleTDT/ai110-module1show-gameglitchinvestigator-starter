# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

Guessing any number gave me the prompt "Go lower". Attempts to press new game did not work. Does not matter if I won or lost. Changing to a new game mode did not create a new game or change the range of numbers on the main prompt.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |

|Guess of 40 |Go Lower |Go Higher |Doesn't recognize the number it choose |

|Clicked new game |Restarts game attempts and number based on difficulty |Does nothing |Doesn't reset what it needs to |

|Game over |Main screen should show 0 attempts remaining |Shows 1 attempt remaining |Attempt script changes after the next attempt it submitted |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude to look over the code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
I asked for an explanation in the code, and the AI told me that part of the code was randomly changing the inputs to string. That explained why the messages also changed on every guess. I deleted the unneccesary lines and only got the messages meant for interger guesses after that.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
When I asked why the range for numbers was always set to 1 to 100, the AI explained it through the difficulty, but only acknowledged Normal. I had to specify why the it didn't change for Easy and Hard, and it changed to fit the request. I made sure to specify those particular requests after.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Since most of the bugs I fixed were logic based, I ran the game and played through to if that portion had been fixed. Sometimes when the AI had helped me fix the code, it would ask to run tests on what I had just fixed. When that happened, I didn't have to go to the game to test it, but I still would.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
I didn't really know which part of the code was messing with the new game functions, so every time I fixed a likely candidate, I would run through the game. Manually playing the game again made me realize how many more errors there were. It's the main reason I kept doing it. It makes me become more thorough in my fixes.
- Did AI help you design or understand any tests? How?
After doing a few fixes in the code, I asked the AI to design tests based on the comments I left in the code. It asked if I wanted to refactor the app code to be testable, and I declined. Once the AI had written the test cases, I read through the tests to make sure I understood what it was testing.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
