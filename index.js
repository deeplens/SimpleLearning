// alexa-cookbook sample code



// There are three sections, Text Strings, Skill Code, and Helper Function(s).

// You can copy and paste the entire file contents as the code for a new Lambda function,

//  or copy & paste section #3, the helper function, to the bottom of your existing Lambda code.





// 1. Text strings =====================================================================================================

//    Modify these strings and messages to change the behavior of your Lambda function

var myBucket = 'your-bucket';      // replace with your own bucket name!

var myObject        = 'deeplens/simplelearning/admin/state/currentstate.txt';         
var myRequestObject = 'deeplens/simplelearning/admin/state/requestedstate.txt';



// 2. Skill Code =======================================================================================================





var Alexa = require('alexa-sdk');



exports.handler = function(event, context, callback) {

    var alexa = Alexa.handler(event, context);

    alexa.appId = 'amzn1.ask.skill.24f3616b-fbd9-4a15-b94a-772d367bbd3d'; // Replace with your own

    // alexa.dynamoDBTableName = 'YourTableName'; // creates new table for session.attributes


    alexa.registerHandlers(handlers);
    alexa.execute();
};



var handlers = {

    'LaunchRequest': function () {
        this.emit(':ask', "What would you like me to do");
        //this.emit('StartTrainingIntent');
    },


    'StartTrainingIntent': function () {
        var myParams = {
            Bucket: myBucket,
            Key: myRequestObject,
            Body: "Training Requested"
        };

        S3write(myParams,  myResult => {
                console.log("sent     : " + JSON.stringify(myParams));
                console.log("received : " + myResult);
                this.response.speak('Deep Lens Simple Training has started. ');
                this.emit(':responseReady');
            }
        )
    },

    'StartDetectionIntent': function () {
        var myParams = {
            Bucket: myBucket,
            Key: myRequestObject,
            Body: "Detection Requested"
        };

        S3write(myParams,  myResult => {
                console.log("sent     : " + JSON.stringify(myParams));
                console.log("received : " + myResult);
                this.response.speak('Deep Lens detection has started.');
                this.emit(':responseReady');
            }
        )
    },


    'GetCurrentStateIntent': function () {
        var myParams = {
            Bucket: myBucket,
            Key: myObject
        };

        S3read(myParams,  myResult => {
                console.log("sent     : " + JSON.stringify(myParams));
                console.log("received : " + myResult);
                this.response.speak('The current status of Deep Lens is, ' + myResult );
                this.emit(':responseReady');
            }
        );
    },



    'AMAZON.HelpIntent': function () {
        var reprompt = 'Say hello or write a file to S 3.';
        this.response.speak('Welcome to s3 file whisperer. ' + reprompt).listen(reprompt);
        this.emit(':responseReady');
    },

    'AMAZON.CancelIntent': function () {
        this.response.speak('Goodbye!');
        this.emit(':responseReady');
    },

    'AMAZON.StopIntent': function () {
        this.response.speak('Goodbye!');
        this.emit(':responseReady');
    },

    'SessionEndedRequest': function () {
        console.log('session ended!');
        this.emit('AMAZON.StopIntent');
    }

};



//    END of Intent Handlers {} ========================================================================================

// 3. Helper Function  =================================================================================================


function S3read(params, callback) {
    var AWS = require('aws-sdk');
    var s3 = new AWS.S3();

    s3.getObject(params, function(err, data) {
        if(err) { console.log(err, err.stack); }
        else {
            var fileText = data.Body.toString();  // this is the complete file contents
            callback(fileText);
        }
    });
}
    
    
    
function S3write(params, callback) {
    var AWS = require('aws-sdk');
    var s3 = new AWS.S3();
    s3.putObject(params, function(err, data) {
        if(err) { console.log(err, err.stack); }
        else {
            //data.Body = "Training Requested";
            var fileText = params.Body;  // this is the complete file contents
            //var fileText = "Training has started";
            callback(fileText);
        }
    });
}
