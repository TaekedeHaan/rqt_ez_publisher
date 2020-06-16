# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:47:28 2020

@author: taeke
"""

import rospy


class TopicSubscriber(object):

    def __init__(self, topic_name, message_class, timeout = 0.5):
        self._name = topic_name
        try:
            self._message = rospy.wait_for_message(topic_name, message_class, 
                                                   timeout = timeout)

        except rospy.exceptions.ROSException as e:
            rospy.loginfo('Did not receive a message on topic %s within a timeout of %s, continuing using default initial values', topic_name, timeout)
            self._message = message_class()
            
        except rospy.exceptions.ROSInterruptException as e:
            raise e
              
    def get_topic_name(self):
        return self._name

    def get_message(self):
        return self._message
