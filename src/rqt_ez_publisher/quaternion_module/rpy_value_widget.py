import tf.transformations
import rospy
from ..widget import double_value_widget
from .. import ez_publisher_model as ez_model


class RPYValueWidget(double_value_widget.DoubleValueWidget):

    def __init__(self, topic_name, attributes, array_index, publisher, 
                 rpy_index, parent, q_init=None):
        self._type = 'RPY'
        self._rpy_index = rpy_index

        rpy_init = tf.transformations.euler_from_quaternion([q_init.x, q_init.y, q_init.z, q_init.w])
        initial_value = rpy_init[rpy_index]
        if self._rpy_index == 0:
            title = ez_model.make_text(
                topic_name, attributes + ['roll'], array_index)
        elif self._rpy_index == 1:
            title = ez_model.make_text(
                topic_name, attributes + ['pitch'], array_index)
        elif self._rpy_index == 2:
            title = ez_model.make_text(
                topic_name, attributes + ['yaw'], array_index)
        else:
            rospy.logerr('this is impossible, rpy[%d]' % rpy_index)
            title = ez_model.make_text(
                topic_name, attributes + ['???'], array_index)
        
        self._initial_value =   initial_value      
        super(RPYValueWidget, self).__init__(
            topic_name, attributes, array_index, publisher, parent,
            label_text=title, initial_value=initial_value)

    def publish_value(self, value):
        q_msg = ez_model.get_msg_attribute_value(self._publisher.get_message(),
                                                 self._topic_name, self._attributes)
        rpy = tf.transformations.euler_from_quaternion(
            [q_msg.x, q_msg.y, q_msg.z, q_msg.w])
        rpy_list = list(rpy)
        rpy_list[self._rpy_index] = value
        new_q = tf.transformations.quaternion_from_euler(
            rpy_list[0], rpy_list[1], rpy_list[2])
        xyzw = 'xyzw'
        for i in range(4):
            ez_model.set_msg_attribute_value(
                self._publisher.get_message(), self._topic_name, self._type,
                self._attributes + [xyzw[i]], self._array_index, new_q[i])
        self._publisher.publish()
