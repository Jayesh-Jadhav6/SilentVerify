import requests
import json
import random
import time

def generate_bot_data(num_sessions=50):
    url = "http://127.0.0.1:5000/submit-data"
    
    print(f"🤖 Generating {num_sessions} bot sessions...")
    
    for i in range(num_sessions):
        fake_data = {
            "userAgent": "FakeBotAgent/1.0",
            "language": "en-US",
            "screenWidth": 800,
            "screenHeight": 600,
            "timeOnPage": random.uniform(0.5, 2.0),  # bots stay very short
            "mouseMoves": [],  # no mouse movement
            "clicks": [],      # no clicks
            "scrolls": [],     # no scrolls
            "label": "bot"
        }

        try:
            response = requests.post(
                url, 
                data=json.dumps(fake_data), 
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print(f"✅ Bot session {i+1}/{num_sessions} sent")
            else:
                print(f"❌ Failed to send bot session {i+1}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error sending bot session {i+1}: {e}")
            
        time.sleep(0.1)  # Small delay to avoid overwhelming server
    
    print("🎉 Bot data generation complete!")

if __name__ == "__main__":
    generate_bot_data()