import requests
import json

def emotion_detector(text_to_analyze):
    URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }
    response = requests.post(URL, json = input_json, headers=header)
    formated_response = json.loads(response.text)

    if response.status_code == 200:
        return formated_response
    elif response.status_code == 400:
        formated_response = {
                            'anger': None,
                            'disgust': None, 
                            'fear': None, 
                            'joy': None, 
                            'sadness': None, 
                            'dominant_emotion': None}
        return formated_response

def emotion_predictor(detected_text):
    if isinstance(detected_text, dict):  # Check if detected_text is already a dictionary
        if 'emotionPredictions' in detected_text:
            emotions = detected_text['emotionPredictions'][0]['emotion']
            anger = emotions.get('anger')
            disgust = emotions.get('disgust')
            fear = emotions.get('fear')
            joy = emotions.get('joy')
            sadness = emotions.get('sadness')
            max_emotion = max(emotions, key=emotions.get)
            formatted_dict_emotions = {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness,
                'dominant_emotion': max_emotion
            }
            return formatted_dict_emotions
        else:
            return {"error": "Invalid dictionary format: 'emotionPredictions' key not found."}
    elif isinstance(detected_text, str):
        try:
            detected_text_dict = json.loads(detected_text)  # Convert JSON string to dictionary
            if 'emotionPredictions' in detected_text_dict:
                emotions = detected_text_dict['emotionPredictions'][0]['emotion']
                anger = emotions.get('anger')
                disgust = emotions.get('disgust')
                fear = emotions.get('fear')
                joy = emotions.get('joy')
                sadness = emotions.get('sadness')
                max_emotion = max(emotions, key=emotions.get)
                formatted_dict_emotions = {
                    'anger': anger,
                    'disgust': disgust,
                    'fear': fear,
                    'joy': joy,
                    'sadness': sadness,
                    'dominant_emotion': max_emotion
                }
                return formatted_dict_emotions
            else:
                return {"error": "Invalid JSON format: 'emotionPredictions' key not found."}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format."}
    else:
        return {"error": "Input is not a valid dictionary or JSON string."}