from traceback import print_tb
from flask import Flask, render_template,request,jsonify
from flask_cors import CORS,cross_origin
import pickle
import os
import numpy as np


app=Flask(__name__)  # Intialize Flask app

@app.route('/', methods=['GET'])  #Route to Display home page   
@cross_origin()
def homePage():
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST']) #Route to show predicted results page
@cross_origin()
def price_predict():
    if request.method == 'POST':

        age=float(request.form['age'])  
        yrs_married=float(request.form['yrs_married'])
        children=float(request.form['children'])
        education=float(request.form['education']) 

        ##ordinal values
        religious=float(request.form['religious'])
        marriage=float(request.form['marriage'])
        
        occupation=float(request.form['occupation'])
        h_occupation=float(request.form['h_occupation'])

        ##Array for ordinal values
        occ_=np.zeros(5)
        h_occ_=np.zeros(5)

        # feature development for womens occupation
        if occupation == 1:
            pass
        else: 
            occ_[int(occupation)-2]=1.0
        
        # feature development for husband occupation
        if h_occupation == 1:
            pass
        else: 
            h_occ_[int(h_occupation)-2]=1.0

        non_scaled_features=np.append(np.append(occ_,h_occ_),[marriage, age,yrs_married,children,religious,education])

        
        model_filename='LR_model.pkl'
        currentpath=os.getcwd()
        final_model_filepath=os.path.join(currentpath, model_filename)
        
        
        lr_affair_model=pickle.load(open(final_model_filepath,'rb')) # loading the model file from the storage
        # predictions using the loaded model file

        #feaures_nonscale=[crim,zn,indus,chas,nox,rm, age,dis,rad,ptratio,b,lstat]
        prediction=lr_affair_model.predict_proba([non_scaled_features])

        print(non_scaled_features)
        print()
        print(non_scaled_features.shape )
        print(prediction)
        print()
        print(prediction[0][0])
        
        
        final_prediction_percentage= prediction[0][0]*100

        return render_template('result.html',prediction="{:.2f}".format(final_prediction_percentage))
if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app