from twilio.twiml.messaging_response import MessagingResponse
import uuid
import hashlib
from logging.handlers import RotatingFileHandler
import logging
from twilio.rest import Client
from flask import Flask, request, jsonify
import time
import datetime
import uuid

from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()
app = Flask(__name__)

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

logging.basicConfig(level=logging.INFO,
                    filename='app.log',#The file to log into  
                    filemode='a',  # Append Logs to existing log file, or use 'w' for a new file every time
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


#To ensure that your log files do not grow too large,
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)# Will rotate the log files, keeping the file size under 10,000 bytes and keep a max of 3 log files
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger('').addHandler(handler)



def getPhoneNumbersOfAvailableStaffs(list_type):
    logging.info("Acquiring phone Numbers from DB")

    # Needs to Updated with DB INFO
    if list_type == 'available':
        # Query for available staff phone numbers
        return ['+', '+']
    elif list_type == 'rejected':
        # Query for rejected staff phone numbers
        return ['+', '+']
    elif list_type == 'winner':
        # Query for winner staff phone numbers
        return ['+']
    else:
        return []


@app.before_first_request
def start_scheduler():
    if not scheduler.running:
        scheduler.start()

@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    if scheduler.running:
        scheduler.shutdown()

@app.route('/getCancelShift', methods=['POST'])
def cancelShift():
    data = request.json
    requestID = data.get('requestID')

    if not requestID:
        logging.error("No requestID provided in the cancel request")
        return jsonify({'status': 'failed', 'message': 'RequestID is required.'}), 400

    else:
        logging.info(f"Shift {requestID} has been Successfully Canceled")
        # Query DB to delete and handle all future messages to that RequestID appropriately

        return jsonify({'status': 'success', 'message': 'Shift request CANCELED successfully.'}), 200


@app.route('/getOpenShiftRequests', methods=['GET'])
def getOpenShiftRequests():
    #Data From DB
    logging.info("Sending list of all Open Shift Requests to App")

    shift_requests = [
        {
            'requestID': "48464684",

            'position': "Doctor",
            'date': "2023-12-01",  # ISO format date
            'fromTime': "09:00",
            'toTime': "17:00",
            'replyDeadline': "2023-11-25T17:30:00",  # ISO format datetime
            'currentBids': "5",

        },
        {
            'requestID': "48464684",

            'position': "Nurse",
            'date': "2023-12-02",
            'fromTime': "08:00",
            'toTime': "16:00",
            'replyDeadline': "2023-11-26T17:30:00",
                        'currentBids': "55",

        },
        {
            'requestID': "48464684",
            'position': "NeuroSurgeon",
            'date': "2023-12-08",
            'fromTime': "08:00",
            'toTime': "16:00",
            'replyDeadline': "2023-12-2T17:30:00",
                        'currentBids': "1",

        },
        {
            'requestID': "48464684",
            'position': "Physicist",
            'date': "2023-12-02",
            'fromTime': "08:00",
            'toTime': "16:00",
            'replyDeadline': "2023-11-26T17:30:00"
        },

    ]
    return jsonify(shift_requests)

@app.route('/getScheduledShiftRequests', methods=['GET'])
def getScheduledShiftRequests():
    #Data From DB
    logging.info("Sending list of all Scheduled Shift Requests to App")

    shift_requests = [
        {
            'position': "Doctor2",
            'date': "2023-12-01",  
            'fromTime': "09:00",
            'toTime': "17:00",
            'assignedToName':'Hisham2'

        },
        {
            'position': "Nurse",
            'date': "2023-12-02",
            'fromTime': "08:00",
            'toTime': "16:00",
            'assignedToName':'Hisham'


        },
        {
            'position': "NeuroSurgeon",
            'date': "2023-12-08",
            'fromTime': "08:00",
            'toTime': "16:00",
            'assignedToName':'Hisham'

        },
        {
            'position': "Physicist",
            'date': "2023-12-02",
            'fromTime': "08:00",
            'toTime': "16:00",
            'assignedToName':'Hisham'

        },

    ]
    return jsonify(shift_requests)




@app.route('/')
def hello():
    return "Shift Management System"

def sendSMS(sender,messageSend):
    message = client.messages.create(
            body=messageSend, 
            from_='+15075735578',
            to=sender
    )
    logging.info("SMS Details:",message.sid,'Status:',message.status,'Date Sent:',message.date_sent)



@app.route('/shiftCreation', methods=['POST'])
def shiftCreate():
    data = request.json

    #Extract the data with default values if not provided
    position = data.get('position', 'Default Position')
    selected_date = datetime.fromisoformat(data.get('selectedDate', 'Default Date')).strftime("%Y-%m-%d")
    reply_deadline = data.get('replyDeadline', 'Default Reply Deadline')
    from_time = data.get('fromTime', 'Default From Time')
    to_time = data.get('toTime', 'Default To Time')

    requestID = generateUniqueRequestId()

    messageBody = (f"You have received a Shift Position:\n"
                    f"To accept request respond with:\nACCEPT {requestID}\n\n"
                    f"Shift Request ID: {requestID}\n"
                    f"Position: {position}\n"
                    f"Date: {selected_date}\n"
                    f"From Time: {from_time}\n"
                    f"To Time: {to_time}\n"
                    f"Respond By: {reply_deadline}")

    for number in getPhoneNumbersOfAvailableStaffs("available"):
        sendSMS(number, messageBody)
    logging.info("Shift has been Successfully created")

    #This Shift needs then to be stored inside DB
    return jsonify({'status': 'success', 'message': 'Shift request sent successfully.'}), 200


def generateUniqueRequestId(length=8):
    unique_id = uuid.uuid4()
    int_id = int(unique_id.int)
    numeric_id = str(int_id)[:length]

    return numeric_id









@app.route('/sms_webhook', methods=['POST'])
def sms_webhook():
    logging.info("Accepting SMS message from user")

    messageBody = request.form['Body']
    sender = request.form['From']

    if messageBody.upper().startswith("ACCEPT"):# Checking if the message is according to format
        return acceptMessage(messageBody, sender)
    else:
        return defaultResponse(sender)






def acceptMessage(message, sender):

    parts = message.split()
    if len(parts) >= 2:
        requestIDFromUser = parts[1]
        #make DB calls
        if(requestIDFromUser=="CHECK DB if its a valid RequestID and respond accodingly"):
            if(requestIDFromUser=="If requestID HASNT BEEN CANCELED"):
                logging.info("Confirming to user that they have applied to shift")
                currentBids=5#DB Data
                dateTime= "2023-11-26T17:30:00"#DB Data

                confirmationMessage(sender,currentBids,dateTime)

                respondByDateTime='THE Respond By DATE AND TIME FOR THE RequestID'# GET FROM DB, needs to be in Datetime format, should acccept in this format
                scheduleShiftMessages(respondByDateTime,requestIDFromUser)
            else:
                logging.info("Informing user that RequestID shift has been canceled")

                sendSMS(sender, "The Requested Shift has been canceled. Thank you for applying.")


        else:
            logging.info("Request ID given is not valid, Informed user to send a valid response")
            sendSMS(sender, "Request ID given is not valid. Please send a valid response:\nACCEPT <RequestID>")# When the give RequestID is not found in DB

        

    else:
        logging.info("Informing user they sent an Unrecognized command, not in the specified format")
        defaultResponse(sender)

    return jsonify(status='success'), 200


def scheduleShiftMessages(respondByDateTime,requestID):
    logging.info("Scheduling Messages")
    respondByDateTime = datetime(2023, 12, 10, 15, 30)#When testing to teh datetime+10min fromNow

    scheduler.add_job(shiftWinnerMessage, 'date', run_date=respondByDateTime, args=[requestID])
    scheduler.add_job(rejectionMessage, 'date', run_date=respondByDateTime)





















def shiftWinnerMessage(requestID):
    #Needs to Updated with DB INFO using Given RequestID#############################


    position ="Doctor" #data.get('position')
    selected_date ="5/12/2023" #data.get('selectedDate')
    from_time = "07:00"#data.get('fromTime')
    to_time = "19:00"#data.get('toTime')
    request_id = 54168413  # Replace with actual request ID

    # Create the SMS message
    messageBody = (f"Shift Request ID: {request_id} has been confirmed\n"
                    f"Position: {position}\n"
                    f"Date: {selected_date}\n"
                    f"From Time: {from_time}\n"
                    f"To Time: {to_time}\n")

    # Send the message to each phone number
    shiftWinnerNumber=getPhoneNumbersOfAvailableStaffs('winner')

    for number in shiftWinnerNumber:# There should be just 1 number
        sendSMS(number,messageBody)

    return jsonify({"message": "Shift request received and SMS sent"}), 200





def rejectionMessage():
    numbers=getPhoneNumbersOfAvailableStaffs('rejected')

    for number in numbers:
        sendSMS(number, "Unfortunetly the shift was assigned to another staff number. Thank you for applying, we appreciate it.")

    return jsonify(status='success'), 200

def defaultResponse(sender):
    logging.info("Sending SMS message back to user, concerning Unrecognized command")

    sendSMS(sender, "Unrecognized command. Please send a valid response:\nACCEPT <RequestID>")
    return jsonify(status='success'), 200


def confirmationMessage(sender,currentBids,dateTime):
    logging.info("Sending corfirmation SMS message back to user")

    sendSMS(sender, "Thank you for applying for the shift. There are "+currentBids+" other staff members who have applied as well.\nYou will be notified at "+ dateTime+" on the results.")
    return jsonify(status='success'), 200




if __name__ == "__main__":
    app.run(debug=True)
    