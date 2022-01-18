'use strict';
/**
 * This is a sample Lambda function that sends an SMS Notification When your
 * Deep Lens Simple Learning sends it.
 * 
 * 
 * Update the phone number or TopicARN environment variable. */

const AWS = require('aws-sdk');
const phone_number = process.env.phone_number;
const SNS = new AWS.SNS({
	apiVersion: '2010-03-31'
});
exports.handler = (event, context, callback) => {
	console.log('Received event:', event);
	if(event.key == "DeepLens Simple Learning") {
		var prob1 = event.Obj1Prob;
		var prob1Float = parseFloat(prob1)
		var obj1 = prob1Float.toFixed(0);
		var prob2 = event.Obj2Prob;
		var prob2Float = parseFloat(prob2)
		var obj2 = prob2Float.toFixed(0);
		const obj1String = obj1 + "% :  " + event.Label1
		const obj2String = obj2 + "% :  " + event.Label2
		const message = "Simple Learning Detection" + "\n" + event.URL + "\n" + obj1String + "\n" + obj2String;
		const params = {
			Message: message,
			TopicArn: "arn:aws:sns:us-east-1:your-account:DeepLensSimpleLearning" // Change this to your own.
		}
		SNS.publish(params, callback);
	}
};
