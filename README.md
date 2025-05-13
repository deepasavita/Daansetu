# Daansetu - Donation Platform for NGOs

**Daansetu** is a Django-based web application designed to connect donors, volunteers, and NGOs. The platform facilitates the donation of essential items and funds to support those in need. Whether it’s clothes, food, electronics, or other critical items, **Daansetu** allows individuals to contribute to various causes seamlessly.

## Key Features

- **Admin Panel** to manage donations, campaigns, users, and volunteers.
- **Donors** can donate money or physical items such as food, clothes, books, and electronics.
- **Volunteers** can view and manage donation pickups and deliveries.
- **Real-time Tracking** of donation status (Pending, Approved, Picked Up, Delivered).
- **Diverse Donation Categories** including:
  - **Food**: Grains, snacks, canned goods
  - **Clothing**: Shirts, sweaters, jackets, etc.
  - **Electronics**: Phones, laptops, chargers, etc.
  - **Books & Stationery**: School books, pens, notebooks, etc.
  - **Toys & Health Products**: Baby toys, diapers, sanitary products
  - **Household Items**: Kitchenware, utensils, bedsheets, etc.

## How It Works

1. **Donors** can create an account, choose the donation type, and submit details about the items or money they wish to donate.
2. **Volunteers** will be assigned to pickup the donated items and ensure they reach the designated NGO or recipient.
3. **Admins** can manage all aspects of the platform, from user management to overseeing donations and volunteer activities.

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS (Bootstrap for responsive design)
- **Database**: SQLite (with potential for migration to PostgreSQL or MySQL)
- **Admin Panel**: Django Admin
- **Authentication**: Django’s built-in User model with extended profile for roles

## Target Users

- **Donors**: Anyone who wants to donate essential items or funds to those in need.
- **Volunteers**: Individuals who help with the pickup and delivery of donations.
- **NGOs**: Organizations that receive and distribute the donations.

## Future Enhancements

- Integration with **payment gateways** for monetary donations.
- A **rating and review system** for donors and volunteers.
- Ability to track **donation impact** (e.g., how many families were helped).

## License

This project is licensed under the **MIT License**.

