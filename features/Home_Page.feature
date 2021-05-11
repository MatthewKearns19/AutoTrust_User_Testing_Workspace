Feature:Home page navigation feature

  Scenario Outline: Navigate to our Home page and test the UI
    When The user navigates to the <homepage_url>
    Then the user can see the <welcome_text>
    And the user visually compares the <screenshotted_page>

    Examples:
    #This is calling our netlify hosted url
    | homepage_url                               | welcome_text                                                                | screenshotted_page |
    | https://auto-trust-user-workspace-staging-demo.netlify.app/  | Welcome to AutoTrust, the home of all your automated visual testing desires.| homepage           |
