Feature:Home page navigation feature

  Scenario Outline: Navigate to our Home page and test the UI
    When The user navigates to the <homepage_url>
    Then the user can see the <heading_text>
    And the user visually compares the <screenshotted_page_location>
    And the the location contains an image so assess the image quality <screenshotted_page_location>

    Examples:
    #This is calling our hosted url
    | homepage_url                                                 | heading_text                                                 | screenshotted_page_location |
    | https://auto-trust-user-workspace-staging-demo.netlify.app/  | Welcome to Auto-Trust, a visual testing automation framework.| landing_page                |
