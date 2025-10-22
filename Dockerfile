# Use the official Python runtime image
FROM python:3.13  

# Create the app directory
RUN mkdir /WCHDApp

# Set the working directory inside the container
WORKDIR /WCHDApp

# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

# Upgrade pip
RUN pip install --upgrade pip 

#So we can use psql tools
RUN apt-get update && apt-get install -y postgresql-client

# Copy the Django project  and install dependencies
COPY requirements.txt  /WCHDApp/

# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project to the container
COPY . /WCHDApp/

# Expose the Django port
EXPOSE 8000

# Run Django’s development server
#First CMD line is for development builds, second is for produciton builds
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "WCHDProject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]

