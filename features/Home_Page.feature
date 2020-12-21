Feature:Home page navigation feature

  Scenario Outline: Navigate to our Home page and test the UI
    When The user navigates to the <homepage_url>
    Then Then the user can see the <welcome_text>

    Examples:
    | homepage_url                               | welcome_text                                                                |
    | https://userworkspaceexample.netlify.app/  | Welcome to AutoTrust, the home of all your automated visual testing desires.|
    #This is calling our netlify hosted url