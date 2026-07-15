Feature: Login Functionality
  As a user of Rahul Shetty Academy
  I want to login to the practice site
  So that I can access my dashboard

  Background:
    Given the application is open

  Scenario: Login with invalid credentials
    When User enters invalid email "test@wrong.com" and password "WrongPass@123"
    And User clicks on the login button
    Then User should see an error message "Incorrect email or password."

  Scenario: Login with empty fields
    When User leaves the email field empty and password field empty
    And User clicks on the login button
    Then User should see validation messages for both fields
    And The login should not be successful

  Scenario: Navigate to registration page
    When User clicks on the "Register here" link
    Then User should be redirected to the registration page
    And The URL should contain "/client/#/auth/register"

  Scenario: Verify password masking
    When User enters password "Test@123" in the password field
    Then The password should be displayed as dots or asterisks
    And The password value should not be visible as plain text

  Scenario: Successful login and dashboard access
    When User enters valid email "aslamwaqar313@gmail.com" and password "Password@11"
    And User clicks on the login button
    Then User should be redirected to the dashboard page
    And The dashboard should display "Home" and "Search" navigation links