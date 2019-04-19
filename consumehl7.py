#!/usr/bin/python
# -*- coding: utf-8 -*-
import hl7apy
from hl7apy.parser import parse_message
from hl7apy.parser import parse_segment, parse_field, parse_component
from pprint import pprint
import string
import json


# raw_string = "MSH|^~\\&|||||20160824132224||ADT^A04^ADT_A01|30353BBD50C9B8D2|P|2.4\rEVN|A04|201608241322\rPID|||X551N15L6G9Y189^5^M11||sdfsdfsdf^dsnfdnfisod^Mr||20160824|M|||^^^qweqweqw^234567||123123|||1\rPV1|1|I|2000^2012^01||||004777^LEBAUER^SIDNEY^J.|||SUR||||1|A0"

def lambda_handler(event, context):

    hl7_message = event['hl7']
    message = parse_message(hl7_message)
    response = {
        'PatientID': message.pid.pid_3.pid_3_1.value,
        'City': message.pid.pid_11.pid_11_3.value,
        'Country': message.pid.pid_11.pid_11_6.value,
        'DateOfBirth': message.pid.pid_7.value,
        'FirstName': message.pid.pid_5.pid_5_2.value,
        'Gender': message.pid.pid_8.value,
        'LastName': message.pid.pid_5.pid_5_1.value,
        'MaritalStatus': message.pid.pid_16.value,
        'MiddleName': ' ',
        'ResidenceNumber': message.pid.pid_11.pid_11_1.value,
        'Salutation': message.pid.pid_5.pid_5_3.value,
        'State': message.pid.pid_11.pid_11_4.value,
        'ZipCode': message.pid.pid_11.pid_11_5.value,
        'Allergies': message.al1.al1_3.al1_3_2.value
        }


    return response











