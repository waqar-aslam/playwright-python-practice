Feature: Login

  Background:
    Given the application is open

  Scenario: Login with valid credentials
    Given the user is on the login page
    When the user enters username "aslamwaqar313@gmail.com" and password "Password@11"
    And clicks the Sign In button
    Then the dashboard should be displayed