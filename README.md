# DiceBot AWS Lambda Function
Creates a `/roll` dice roll command for Slack.

# Lambda Configuration
- Runtime: Python 2.7
- Handler: lambda_function.lambda_handler
- Role: Choose an existing role
- Existing role: lambda_basic_execution
- Description: DiceBot /roll

# Lambda Trigger
### API Gateway
- Method: ANY
- Authorization: None (Open)

# Slack Configuration
- Add a custom Slash Command
- Point the Slash Command to the API Gateway URL (Lambda Trigger)
- Method: POST
- Customized Name: DiceBot
- Usage Hint: "[dice] d [sides] vs [difficulty] e.g. 2d6 vs 8"
