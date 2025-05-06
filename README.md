# NIDS

This project is a Network Intrusion Detection System which does Anomaly Based Detection tailored towards IoT systems.



## Important Files

### Prediction
[tuesday-Copy1.ipynb](tuesday-Copy1.ipynb) -  train and save the CNN model\
[load_model.ipynb](load_model.ipynb) - load the CNN and perform inference\
[load_model.py](load_model.py) - only required steps to save inference results

[1st_attempt.ipynb](final/1st_attempt.ipynb) - preprocessing

[final/PSO_logistic.ipynb](final/PSO_logistic.ipynb) - LR using PSO\
[final/logistic_inference.ipynb](final/logistic_inference.ipynb) - LR inference\
[final/logistic_inference_script.py](final/logistic_inference_script.py) - LR inference script

[final/combine.ipynb](final/combine.ipynb) - Combine results of both models\
[final/mode_mode.py](final/mode_mode.py), [min_min.py](final/min_min.py), [mode_min.py](final/mode_min.py) - Combine scripts for different methods


### Normal Traffic
[final_with_temp/final_with_temp.ino](final_with_temp/final_with_temp.ino)


### Attack (ESP8266 NodeMCU)
[esp8266tokalilinux.ino](esp8266tokalilinux.ino)


### MQTT Server used
[TankFill](https://github.com/roshan-nahsor/TankFill)




## Usage

### Virtual Environment
Use any method to create a python virtual environement.
For using a virtual environment with JupterLab refer this [video](https://youtu.be/9LIWqWSABHc).

### Requirements
`pip install -r final/requirements.txt`

