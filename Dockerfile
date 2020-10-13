FROM robolab.innopolis.university:5000/face_rec

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends python3-dev

RUN python3 -m pip install -Ur requirements.txt
RUN source /opt/intel/computer_vision_sdk/bin/setupvars.sh
