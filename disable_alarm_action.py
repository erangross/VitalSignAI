import boto3

# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch')

# Disable alarm
cloudwatch.disable_alarm_actions(
  AlarmNames=['Web_Server_CPU_Utilization'],
)