import asyncio
import os
import tempfile
import time

import edge_tts
import pygame
import speech_recognition as sr


recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
pygame.mixer.init()


def listen():
    with sr.Microphone() as source:
        print("\nListening... Speak now.")
        recognizer.adjust_for_ambient_noise(
            source, duration=0.4
        )
        try:
            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=15
            )
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None

    # Try Bangla first, then English.
    # Recognition is online and sends audio to the recognition service.
    for language in ("bn-BD", "en-US"):
        try:
            text = recognizer.recognize_google(
                audio, language=language
            )
            if text.strip():
                print(f"You [{language}]: {text}")
                return text.strip()
        except sr.UnknownValueError:
            continue
        except sr.RequestError as exc:
            print("Speech recognition network error:", exc)
            return None

    print("Sorry, I could not understand the speech.")
    return None


def contains_bengali(text):
    return any(
        "\u0980" <= char <= "\u09FF"
        for char in text
    )


async def generate_speech(text, output_file):
    if contains_bengali(text):
        voice = "bn-BD-NabanitaNeural"
    else:
        voice = "en-US-AriaNeural"

    speech = edge_tts.Communicate(
        text=text[:3000],
        voice=voice
    )
    await speech.save(output_file)


def speak(text):
    print(f"\nBondhu AI: {text}")

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".mp3", delete=False
        ) as temp:
            temp_path = temp.name

        asyncio.run(generate_speech(text, temp_path))

        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()

    except Exception as exc:
        print("Voice output failed:", exc)
        print("Please check your internet connection.")

    finally:
        if temp_path:
            try:
                os.remove(temp_path)
            except OSError:
                pass


def shutdown_voice():
    pygame.mixer.quit()