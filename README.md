# Latency_ROS
**Latency measurements for ROS**  

Measure local environment or server delays with the help of Latency tests
</br>
1. **Latency checker for String messages**
   * **Publisher-Subscriber Setup**
   * **Server-Client Setup**
2. **Latency checker for images**
   * **Using USB Cam**
   * **Server-Client Setup**

## Latency Checker for String Messages :
### Publisher-Subscriber Setup:
Run **timer.py** followed by **time_listener.py**

---    
#### Algorithm:
1. **timer.py** initializes a `node` and subsequently a `publisher` on the topic `chatter`

3. **time_listener.py** initializes a `node` and subsequently a `subscriber` on the topic `chatter`
4. For `num_publish` times,
    * The `publisher` in **timer.py** publishes it's `rostime` at that instant
    
    * The `subscriber` in **time_listener.py** subscribes to that message, and in its `callback function`, calls a `publisher` to publish the received string message (`rostime of the publisher in timer.py in step no. 1`) on a topic `rebound_chatter`
    * In **timer.py**, a `subscriber` on the topic `rebound_chatter` is initialized to receive the republished string `rostime`.
    * **Latency** is measures by taking the difference between the `rostime` of the `node` in **timer.py** on the instant of receipt of the republished message by the `subscriber` subscribing to `rebound_chatter`, and the received republished message (`rostime of the publisher in timer.py in step no. 1`) converted to `rostime`.

---
