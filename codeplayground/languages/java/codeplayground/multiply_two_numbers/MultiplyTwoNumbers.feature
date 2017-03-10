Feature: Multiply two numbers

  Scenario Outline: Multiply two numbers
    When I call the calculator service with a equal <num1> and b equal <num2>
    Then the result is <result>

    Examples:
      | num1 | num2 | result |
      | 9    | 8    | 72     |
      | 5    | 4    | 20     |
