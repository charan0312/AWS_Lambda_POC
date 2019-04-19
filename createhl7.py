#!/usr/bin/python
# -*- coding: utf-8 -*-
from hl7apy import core
from hl7apy.core import Message
from hl7apy.consts import VALIDATION_LEVEL
import json
from pprint import pprint
import boto3
import random
import datetime
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')

        # Message Header Segment

    regmsg = core.Message('ADT_A01',
                          validation_level=VALIDATION_LEVEL.STRICT)

    # regmsg.msh.msh_9 = 'ADT^A04^ADT_A01' #CM_MSG.1,CM_MSG.2 (Message Type, Trigger event)

    regmsg.msh.msh_10 = ''.join(random.choice('0123456789ABCDEF')
                                for i in range(16))
    regmsg.msh.msh_11 = 'P'
    regmsg.msh.msh_12 = '2.4'
    regmsg.msh.msh_9.msh_9_1 = 'ADT'
    regmsg.msh.msh_9.msh_9_2 = 'A04'
    regmsg.msh.msh_9.msh_9_3 = 'ADT_A01'

        # Event Segment

    regmsg.evn.evn_1 = 'A04'
    time = datetime.datetime.now()
    regmsg.evn.evn_2 = str(time.strftime('%Y')) + str(time.strftime('%m'
            )) + str(time.strftime('%d')) + str(time.strftime('%H')) \
        + str(time.strftime('%M'))

        # PID Segment
        # regmsg.pid = 'PID|||PATID1234^5^M11||JONES^WILLIAM^A^III||19610615|M||2106-3|1200 N ELM STREET^^GREENSBORO^NC^27401-1020|GL|(919)379-1212'

    table2 = dynamodb.Table('Users')
    subresponse = table2.scan(FilterExpression=Attr('UserID'
                              ).eq(event['PatientID']))

    regmsg.pid.pid_3.pid_3_1 = event['PatientID']  # internal ID
    regmsg.pid.pid_3.pid_3_2 = '5'
    regmsg.pid.pid_3.pid_3_3 = 'M11'

    regmsg.pid.pid_5.pid_5_1 = subresponse['Items'][0]['Details'
            ]['LastName']
    regmsg.pid.pid_5.pid_5_2 = subresponse['Items'][0]['Details'
            ]['FirstName']
    regmsg.pid.pid_5.pid_5_3 = subresponse['Items'][0]['Details'
            ]['Salutation']

    dob = subresponse['Items'][0]['Details']['DateOfBirth']

    regmsg.pid.pid_7 = str(time.strftime('%Y')) + str(time.strftime('%m'
            )) + str(time.strftime('%d'))  # DOB
    regmsg.pid.pid_8 = 'M'  # Gender
    regmsg.pid.pid_11.pid_11_1 = 'Address'
    regmsg.pid.pid_11.pid_11_3 = 'City'
    regmsg.pid.pid_11.pid_11_4 = subresponse['Items'][0]['Details'
            ]['State']
    regmsg.pid.pid_11.pid_11_5 = subresponse['Items'][0]['Details'
            ]['ZipCode']
    regmsg.pid.pid_11.pid_11_6 = 'USA'

    regmsg.pid.pid_13 = subresponse['Items'][0]['Details'
            ]['ResidenceNumber']  # Phone (home)

    regmsg.pid.pid_16 = subresponse['Items'][0]['Details'
            ]['MaritalStatus']  # Marital status

        # Patient Visit Segment

    # regmsg.pv1 = \
    #     'PV1|1|I|2000^2012^01||||004777^LEBAUER^SIDNEY^J.|||SUR||||1|A0'

    regmsg.pv1.pv1_1 = '1'
    regmsg.pv1.pv1_2 = 'I'

        # Insurance info
    # regmsg.in1 = 'IN1|001|A357|1234|BCMD|||||132987'

    # Diagnosis Segment
    regmsg.dg1.dg1_1 = '1' #Set Id - Diagnosis(Type:Sequence Id) (ICD9 is the only valid coding system supported by the interface. This field should contain "I9" if the diagnosis is an ICD9 coded diagnosis. Otherwise, the field should be omitted.)
    regmsg.dg1.dg1_2 = 'I9' #Diagnosis Coding Method(ID) = ICD9
    regmsg.dg1.dg1_6 = 'A' #Diagnosis / Drg Type(ID) {"ADMITTING" A, "INTERIM" P and "FINAL"}


    # Allergies Segment
    regmsg.al1.al1_1 = '1' #Set Id - Allergy(Type:Sequence Id) (4) (Alphanumeric e.g.,00 to 98, A1, etc)
    regmsg.al1.al1_2 = 'MA' #Allergy Type (DA(Drug Allergy), FA(Food Allergy), MA(Misc Allergy)
    #regmsg.al1.al1_3.al1_3_1 = '' #Allergy identifier (optional)
    regmsg.al1.al1_3.al1_3_2 = 'fdfgadfgdfgfdg' #Text
    #regmsg.al1.al1_3.al1_3_3 = 'FDBDAA' #Name Of Coding System (optional)

    regmsg.validate()
    msg = {"message": "SUCCESS", "hl7": regmsg.value}

    return msg
