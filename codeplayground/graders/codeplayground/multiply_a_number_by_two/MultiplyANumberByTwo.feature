Feature: Multiply a number by two

  Scenario Outline: Multiply a number by two
    When I call the calculator service with <x>
    Then the multiplied result is <result>

    Examples:
      | x | result |
      | 0 | 0      |
      | 1 | 2      |
      | 2 | 4      |
