
# TapGenie
A website similar to UrbanClap for booking services with professionals. Has User Interface for both customers and professionals.

**Languages**: HTML/CSS, Javascript, Python, SQL

**Tools**: Figma, Flask, Github, ML APIs

## Project Overview:
TapGenie is a web platform designed to offer a simple and intuitive way for users to book services from various professionals. The website provides services such as home cleaning, beauty, and wellness. Customers can browse service categories, select sub-services, and choose professionals based on ratings and reviews.

## Key Features:
1. **Professional Selection**: Unlike other service platforms where customers only choose the service, TapGenie allows users to choose the professional providing the service.
2. **Dynamic Pricing**: The price of the service is influenced by the base price and the professional’s rating.
3. **Real-Time Availability**: Professional availability is calculated in real-time based on prior appointments.
4. **Login/Signup**: With format checking for all fields and accessing/updating profile
5. **ML API for Translation**: An integrated Machine Learning API allows users to view professional reviews in Hindi, enhancing accessibility.
6. **Personalized Service Selection**: Customers can select the professional providing the service according to their preference.
7. **Real-Time Professional Availability**: The system ensures real-time appointment management, taking into account the professional’s prior appointments.

## Design and Technical Decisions:
1. **Slot-Based Scheduling**: Initially, users could choose any time, but it was replaced with a slot-based approach to simplify handling professional availability and duration uncertainty.
2. **Service-Professional Mapping**: Services are mapped to professions, which in turn are linked to professionals, ensuring flexibility in service management.
3. **Review System**: Reviews are attached to professionals rather than services, as the professional’s performance plays a crucial role in customer satisfaction.

