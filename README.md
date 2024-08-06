# chat_bot
# Project Introduction

This project is a demonstration model of a chatbot designed for a mattress manufacturing company, Bedzone Industries. The chatbot, named "Allu Chatbot," serves as a proof of concept for integrating conversational AI with business operations. The primary objective of the chatbot is to streamline customer interactions by taking orders and tracking them.


# Development Process
     Feature Prioritization: Employed backlog and Minimum Viable Product (MVP) methodologies to identify and prioritize features. The first phase focused on core functionalities—order management and tracking.



Key features include:

    1. **Order Management**: The chatbot can take customer orders, adding order details to a MySQL database. This feature ensures that customer requests are accurately recorded and easily accessible for further processing.

    2. **Order Tracking**: Customers can inquire about the status of their orders, and the chatbot retrieves the relevant information from the database, providing real-time updates.

The backend is built using FastAPI, with the main logic handled in `main.py`. Additional helper modules, such as `generic_helper.py` and `db_helper.py`, assist with session management and database interactions, respectively. The conversational model is trained using Google Dialogflow and connected to the backend via Uvicorn. Secure HTTP tunneling is achieved using Ngrok, and Google Cloud Console is used for credential management and authentication.

The project serves as a preliminary model, showcasing potential capabilities. If Bedzone Industries is interested, the chatbot can be deployed on their website or integrated into public platforms, providing a seamless and automated customer service experience.
The project showcases a comprehensive understanding of backend development, API integration, and conversational AI. It highlights the ability to build scalable applications that interface with modern web technologies and machine learning platforms.