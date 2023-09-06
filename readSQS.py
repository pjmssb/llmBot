import boto3

# Initialize the SQS client
sqs = boto3.client('sqs', region_name='us-east-1')

# The URL is constructed from the ARN, but if you have the direct URL, you can use that too.
queue_url = 'https://sqs.us-east-1.amazonaws.com/337340005201/sqs_llmbot.fifo'

while True:
    # Retrieve messages from SQS
    messages = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=10  # Adjust this number as needed
    )

    # Check if any messages were returned
    if 'Messages' in messages:
        for message in messages['Messages']:
            # Print the message to stdout
            print(message['Body'])

            # Delete the message from the queue so it won't be read again
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
    else:
        # No messages to process
        break

print("Finished reading messages.")
