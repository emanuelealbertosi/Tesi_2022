from flask import Flask, jsonify, request
# initialize our Flask application
app= Flask(__name__)
import boto3
import base64
import io
import time
import json



def start_model(project_arn, model_arn, version_name, min_inference_units):

    client=boto3.client('rekognition','us-east-1')

    try:
       
        print('Starting model: ' + model_arn)
        response=client.start_project_version(ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units)
      
        project_version_running_waiter = client.get_waiter('project_version_running')
        project_version_running_waiter.wait(ProjectArn=project_arn, VersionNames=[version_name])

        #Get the running status
        describe_response=client.describe_project_versions(ProjectArn=project_arn,
            VersionNames=[version_name])
        for model in describe_response['ProjectVersionDescriptions']:
            print("Status: " + model['Status'])
            print("Message: " + model['StatusMessage']) 
    except Exception as e:
        print(e)
        print("ECCEZIONE START")
        
    print('Done...')


def show_custom_labels(model,photo, min_confidence):
    client=boto3.client('rekognition','us-east-1')

    base_64_binary = base64.decodebytes(photo)
    #base_64_binary=photo
    retry=True
    while retry:
        try:
            response = client.detect_custom_labels(Image={'Bytes': base_64_binary},MinConfidence=min_confidence,ProjectVersionArn=model)
            retry=False
        except Exception as e:
            retry=True   
  
   
    return response['CustomLabels']

def stop_model(model_arn):

    client=boto3.client('rekognition','us-east-1')

    print('Stopping model:' + model_arn)

    #Stop the model
    try:
        response=client.stop_project_version(ProjectVersionArn=model_arn)
        status=response['Status']
        print ('Status: ' + status)
    except Exception as e:  
        print(e)  

    print('Done...')


@app.route("/", methods=["POST"])
def postf():
    #######mock
    shop_status={} 
    shop_status=[{"Confidence":92,"Name":"aperto"}]
    return jsonify(shop_status) 
    #######mock
    posted_data = request.get_json()
    photo=posted_data['image']
    project_arn='arn:aws:rekognition:xxxxxxxx'
    model_arn='arn:aws:rekognition:xxxxxxxx'
    min_inference_units=1 
    version_name='xxxxxxxxxx'
    start_model(project_arn, model_arn, version_name, min_inference_units)
    min_confidence=70
    
    label_count=show_custom_labels(model_arn,photo.encode("ascii"), min_confidence)
           
    
    stop_model(model_arn)
    
    
    
    
    return jsonify(label_count)

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')