import os
os.system('pip3 install -r requirements.txt')
os.system('python3 manage.py makemigrations')
os.system('python3 manage.py migrate')
os.system('python3 loadData.py')
os.system('python3 loadPosts.py')
# os.system('python3 manage.py runsever')