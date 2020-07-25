# Latency_ROS
**Latency measurements for ROS**  

Measure local environment or server delays with the help of Latency tests

1. **[Latency checker for String messages](https://github.com/ArusarkaBose/Latency_ROS/blob/master/README.md#latency-checker-for-string-messages-)**
   * **[Publisher-Subscriber Setup](https://github.com/ArusarkaBose/Latency_ROS/blob/master/README.md#publisher-subscriber-setup)**
   * **[Server-Client Setup](https://github.com/ArusarkaBose/Latency_ROS/blob/master/README.md#server-client-setup-)**
2. **[Latency checker for images](https://github.com/ArusarkaBose/Latency_ROS/blob/master/README.md#latency-checker-for-images-)**
   * **[Using USB Cam](https://github.com/ArusarkaBose/Latency_ROS/blob/master/README.md#using-usb-cam)**
   * **[Server-Client Setup](https://github.com/ArusarkaBose/Latency_ROS/blob/master/README.md#server-client-setup)**

## Latency Checker for String Messages :
### Publisher-Subscriber Setup:
Run **timer.py** followed by **time_listener.py**

---    
#### Algorithm:
1. **timer.py** initializes a `node` and subsequently a `publisher` on the topic `chatter`

2. **time_listener.py** initializes a `node` and subsequently a `subscriber` on the topic `chatter`

3. For `num_publish` times,

    * The `publisher` in **timer.py** publishes it's `rostime` at that instant
    
    * The `subscriber` in **time_listener.py** subscribes to that message, and in its `callback function`, calls a `publisher` to publish the received string message (`rostime of the publisher in timer.py in step no. 1`) on a topic `rebound_chatter`
    
    * In **timer.py**, a `subscriber` on the topic `rebound_chatter` is initialized to receive the republished string `rostime`.
    
    * **Latency** is measures by taking the difference between the `rostime` of the `node` in **timer.py** on the instant of receipt of the republished message by the `subscriber` subscribing to `rebound_chatter`, and the received republished message (`rostime of the publisher in timer.py in step no. 1`) converted to `rostime`.

---

### Server-Client Setup :
Run **latencycheckserver.py** followed by **latencycheckclient.py**

---
#### Algorithm:
1.  Create a **server** node and a **client** node

2. The **client** node gets its `rostime` and sends it as a `request` to the **server** node  

3. The **server** node receives the `request` and returns the same as `response` to the **client** node without any change

4. The **client** node measures the difference between its `rostime` at the instant of receipt of the **server** `response` and the `rostime` returned as `response` by the **server** (which is equal to the `rostime` of the **client** at the instant of sending the `service request`)

---

## Latency Checker for Images :
### Using USB Cam:
Run the **usb-cam ros node** using the command:

    rosrun usb_cam_ usb_cam_node __pixel_format:= yuyv

Open a separate shell and execute the script **usbcam_latency_sendback.py**.

---
#### Algorithm:
1. Initialize a **subscriber** to the topic on which the `usb_cam node` publishes

2. In the `callback function`, extract the `rostime` of the setup environment at the instant of publishing of the `usb_cam` image, from the `header stamp` of the image

4. Subtract the same from the current `rostime` of the **subscriber** node

---

### Server-Client Setup:
Run **image_latency_server.py** followed by **image_latency_client.py**
1.  Create a **server** node and a **client** node

2.  The client node gets a frame from the webcam through OpenCV, converts the frame to a `ros-image` and sends it, along with its `rostime`, as a `request` to the **server** node 

3.   The **server** node receives the `request` and returns the same as `response` to the **client** node without any change

5. The **client** node measures the difference between its `rostime` at the instant of receipt of the **server** `response` and the `rostime` returned as part of the `response` by the **server** (which is equal to the `rostime` of the **client** at the instant of sending the `service request`)
---

