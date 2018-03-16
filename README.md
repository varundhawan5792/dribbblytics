sudo pip install -r requirements.txt
redis-server
celery -A tasks worker --loglevel=info  
python main.py
