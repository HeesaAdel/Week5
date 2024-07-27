import openai
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

# إعداد مفتاح OpenAI API
openai.api_key = 'sk-proj-e0XmQ3RJuegfTkovQiiqT3BlbkFJWOIkCthLcrq8Df7bNrhT'

# وظيفة لتحويل الكلام إلى نص
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("تحدث الآن...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='ar-SA')
            print("أنت قلت: " + text)
            return text
        except sr.UnknownValueError:
            print("لم يتم التعرف على الصوت")
            return ""
        except sr.RequestError as e:
            print("خطأ في خدمة التعرف على الصوت؛ {0}".format(e))
            return ""

# وظيفة لاستخدام ChatGPT
def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي يتحدث العربية."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message['content'].strip()
        print("رد ChatGPT: " + reply)
        return reply
    except Exception as e:
        print(f"حدث خطأ أثناء التفاعل مع ChatGPT: {e}")
        return "عذرًا، حدث خطأ أثناء التفاعل مع ChatGPT."

# وظيفة لتحويل النص إلى كلام
def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='ar')
        tts.save("response.mp3")
        playsound("response.mp3")
    except Exception as e:
        print(f"حدث خطأ أثناء تحويل النص إلى كلام: {e}")

if __name__ == "__main__":
    while True:
        # تحويل الكلام إلى نص
        user_input = speech_to_text()
        if user_input == "":
            continue

        # التفاعل مع ChatGPT
        response = chat_with_gpt(user_input)
        print("ChatGPT: " + response)

        # تحويل النص إلى كلام
        text_to_speech(response)
