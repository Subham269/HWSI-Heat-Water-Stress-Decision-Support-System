import os

base = "/Users/sknaszik/Documents/We Build Devs Hackathon/Project Bhumi/hwsi/backend/app"
os.makedirs(base, exist_ok=True)
os.makedirs(f"{base}/engine", exist_ok=True)
os.makedirs(f"{base}/data", exist_ok=True)
os.makedirs(f"{base}/optimizer", exist_ok=True)
os.makedirs(f"{base}/routers", exist_ok=True)

