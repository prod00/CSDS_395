# CSDS_395

**Vision Statement**
We aim to create a better environment not only for the students of the college community, but the
professors as well. Oftentimes, professors are actively seeking research students. Additionally,
students are always actively seeking opportunities to gain experience and prepare for
postgraduate study or employment. With Applicase, we will construct meaningful relationships
amongst the student body and professors. Applicase will make opportunities much more
accessible than the current structure by providing an organized database of available RA and TA
positions, customized to the student's interests. Applicase also uses a centralized “common app”
structure to streamline multiple simultaneous applications and, additionally, prevent professors
from receiving a deluge of unwanted emails. The application will be similar to ones like
LinkedIn and Handshake. The major difference being the nicheness of Applicase being for
CWRU RA and TA positions only. This specification of the job allows for very fine-tuned
features that CWRU can control. Keeping the website to such a specific goal will keep things
very organized for the users, this is the website to check for updates on RA and TA potential
positions. This streamlined approach also keeps the site itself more organized. This website will
also be free for CWRU and the users with no ads and allow CWRU full control over the site for
features they may want to implement.

**Instructions for setup:**
1. Clone the directory
2. cd into CSDS_395 
3. in terminal run "pip install -r requirements.txt"
4. *To Run Live Chat must install docker*
5. https://docs.docker.com/desktop/
6. *Live Chat only* then "docker run -p 6379:6379 -d redis:5"
7. *Live Chat only* then "python -m pip install channels_redis"
8. then "python loadData.py"
9. then "python loadPosts.py"
10. then "python manage.py makemigrations"
11. then "python manage.py migrate"
12. then "python manage.py runserver"
13. click the link that is displayed in terminal
