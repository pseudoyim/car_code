# car_code
Starter code to be used on the Cardboard Car. Clone this repo on the Pi.

## Drive car like an RC car while streaming live video

1. Open up a terminal window and go to your local copy of `car_code`. This will be the **"server"**.

2. Activate the `stellacar` environment. 
```
source activate stellacar
``` 
If you don't have this setup yet, you can create it using the `environment.yml` in this repo. 
(prerequisites: Anaconda or Miniconda and `conda-env`)
```
conda env create --file environment.yml
```
If this fails, just create a conda environment with the specs listed in `environment.yml` and activate it.

3. Turn on your car and open up Terminal. The bash script in there will automatically display the Pi's IP address. Open up another terminal window on your laptop (Command + N) and `ssh` into your Pi. This terminal window will be the **"client"** (i.e. your Pi).
```
ssh pi@<IP address of your Pi>
```

4. Turn on the battery pack that powers the car's motors.

5. Go to the `car_code` repo on your Pi and edit the `client.py` script:
```
sudo nano client.py
```
On line 9, make sure the IP address matches the IP address of your "sever" computer. You can find this by running `ifconfig` in the  **"server"** terminal.

6. In the **"server"** terminal, run `server.py` and wait for the "Listening..." line to display:
```
python server.py
```

7. In the **"client"** terminal window, run `launch.sh`:
```
bash launch.sh
```

8. Wait a few seconds for the video feed to appear on your computer. You should now be able to drive the car using the arrow keys on your keyboard.

## `car.py`
`car.py` can be used as a library to drive the car (e.g. forward, left, right, reverse). Usage example:
```
from car import Drive

d = Drive()

d.forward(1) 	# Number in parentheses is seconds.
d.left(1)
d.right(1)
d.reverse(1)
```

## Bash script to echo Pi's IP address 
It's convenient to have the Pi's LCD screen display its current IP address when you need to ssh into it.

1. On your Pi, in your root directory, create a file called `.ip_show.sh`:
```
touch .ip_show.sh
```

2. Open that file:
```
sudo nano .ip_show.sh
```

3. Add these lines (the IP address should be in the first couple lines in the wlan0 section):
```
echo 'IP address of this Pi:'
ifconfig wlan0 | head -n 2
```
Save and exit (cmd+O, enter, cmd+X).

4. Open your .bashrc:
```
sudo nano .bashrc
```

5. Add the following lines at the bottom:
```
bash .ip_show.sh
```

6. Close terminal window and open a new one. The lines you entered in step 3 should run/appear when the terminal window opens.
