# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:47:28 2020

@author: taeke
"""

import rospy


class TopicSubscriber(object):

    def __init__(self, topic_name, message_class):
        self._name = topic_name
        try:
            self._subsbriber = rospy.Subscriber(
                topic_name, message_class, self.subscriber_cb)
            self._message = message_class()
        except ValueError as e:
            rospy.logfatal('msg file for %s not found' % topic_name)
            raise e
            
    def subscriber_cb(self, message):
        self._message = message
        rospy.loginfo("I heard %s", self._message)

    def get_topic_name(self):
        return self._name

    def get_message(self):
        return self._message
