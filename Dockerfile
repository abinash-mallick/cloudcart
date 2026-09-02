#Pull the image
FROM python:3.12-slim

#Set the work-directory
WORKDIR /app

#Copy the dependencies to work dir.
COPY requirements.txt .

#Install dependencies and Create an user to avoid root privilege
RUN pip install --no-cache-dir -r requirements.txt && useradd -m -s /bin/bash cloudcart

#Copy rest of code to workdir
COPY . .

#Change ownership of the file/Directory
RUN chown -R cloudcart:cloudcart /app

#Switch User
USER cloudcart

#Expose the port used
EXPOSE 5000

#Run the application
CMD ["python3", "app.py"]




