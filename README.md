# Sephora_project

STEPS

Step 1: Run the following command to set up qdrant server

docker pull qdrant/qdrant

To run container use following command.
docker run -p 6333:6333 qdrant/qdrant

Step 2:
Run transformer_model.py. 
(Also, every time you restart quadrant server you will have to run this python file.)


Step 3: (do not stop the terminal which is running)
In new terminal  use below command to build docker.

docker build -t my-streamlit-app .

To check if docker is build use command – 
docker images

To run docker use command - 
docker run -p 8501:8501 my-streamlit-app

In the UI enter skincare concern keywords

