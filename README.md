
# TapGenie
A website similar to UrbanClap for booking services with professionals. Has User Interface for both customers and professionals.

**Languages**: HTML/CSS, Javascript, Python, SQL

**Tools**: Figma, Flask, Github, ML APIs

## Project Overview:
TapGenie is a web platform designed to offer a simple and intuitive way for users to book services from various professionals. The website provides services such as home cleaning, beauty, and wellness. Customers can browse service categories, select sub-services, and choose professionals based on ratings and reviews.

## Key Features:
1. **Professional Selection**: Unlike other service platforms where customers only choose the service, TapGenie allows users to choose the professional providing the service.
2. **Dynamic Pricing**: The price of the service is influenced by the base price and the professional’s rating.
3. **Real-Time Availability**: Professional availability is calculated in real time based on prior appointments.

## Unique Functionalities:
1. **ML API for Translation**: An integrated Machine Learning API allows users to view professional reviews in Hindi, enhancing accessibility.
2. **Personalized Service Selection**: Customers can select the professional providing the service according to their preference.
3. **Real-Time Professional Availability**: The system ensures real-time appointment management, taking into account the professional’s prior appointments.

## Design and Technical Decisions:
1. **Slot-Based Scheduling**: Initially, users could choose any time, but it was replaced with a slot-based approach to simplify handling professional availability and duration uncertainty.
2. **Service-Professional Mapping**: Services are mapped to professions, which in turn are linked to professionals, ensuring flexibility in service management.
3. **Review System**: Reviews are attached to professionals rather than services, as the professional’s performance plays a crucial role in customer satisfaction.

## Challenges:
- Changes in schemas due to evolving features.
- Incorporating template rendering via Flask in the front end.
- Additional web pages needed for feature implementation.

## Limitations:
1. **Location Preferences**: The system currently does not prioritize professionals based on proximity to the customer.
2. **Location-Based Pricing**: There is no location-specific price differentiation at this stage.

## Future Work:
1. **Flexible Slots**: Allow professionals to specify service durations, impacting pricing.
2. **More Customization**: Provide additional customization options for services such as home painting (e.g., color, brand, texture).
3. **Email Verification**: Add OTP-based email verification.
4. **Professional Verification**: Develop a professional proficiency verification matrix.
