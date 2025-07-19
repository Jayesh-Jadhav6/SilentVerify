import requests
import json
import random
import time

def generate_human_data(num_sessions=50):
    url = "http://127.0.0.1:5000/submit-data"
    
    print(f"👥 Generating {num_sessions} human sessions...")
    
    for i in range(num_sessions):
        # Simulate realistic human behavior
        session_duration = random.uniform(8, 40)  # 8-40 seconds on page
        
        # Generate mouse movements (humans move mouse frequently)
        mouse_moves = []
        for t in range(0, int(session_duration * 1000), random.randint(200, 800)):
            mouse_moves.append({
                "x": random.randint(0, 1920), 
                "y": random.randint(0, 1080), 
                "t": t
            })
        
        # Generate clicks (humans click occasionally)
        clicks = []
        num_clicks = random.randint(1, 5)
        for _ in range(num_clicks):
            clicks.append({
                "x": random.randint(0, 1920), 
                "y": random.randint(0, 1080), 
                "t": random.randint(0, int(session_duration * 1000))
            })
        
        # Generate scrolls (humans scroll)
        scrolls = []
        num_scrolls = random.randint(2, 8)
        for _ in range(num_scrolls):
            scrolls.append({
                "y": random.randint(0, 2000), 
                "t": random.randint(0, int(session_duration * 1000))
            })

        fake_data = {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "language": "en-US",
            "screenWidth": 1920,
            "screenHeight": 1080,
            "timeOnPage": session_duration,
            "mouseMoves": mouse_moves,
            "clicks": clicks,
            "scrolls": scrolls,
            "label": "human"
        }

        try:
            response = requests.post(
                url,
                data=json.dumps(fake_data),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print(f"✅ Human session {i+1}/{num_sessions} sent")
            else:
                print(f"❌ Failed to send human session {i+1}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error sending human session {i+1}: {e}")
            
        time.sleep(0.1)  # Small delay
    
    print("🎉 Human data generation complete!")

if __name__ == "__main__":
    generate_human_data()