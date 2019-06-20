#!/usr/bin/env python

import esiaf_channel_utils
import pyesiaf
import rospy
from esiaf_ros.msg import RecordingTimeStamps, AugmentedAudio

# config
import yaml
import sys

# util
import StringIO


def msg_to_string(msg):
    buf = StringIO.StringIO()
    msg.serialize(buf)
    return buf.getvalue()


def msg_from_string(msg, data):
    msg.deserialize(data)


nodename = 'esiaf_splitter'

# initialize rosnode
rospy.init_node(nodename)
pyesiaf.roscpp_init(nodename, [])

# read config
rospy.loginfo('Loading config...')
argv = sys.argv
if len(argv) < 2:
    rospy.logerr('Need path to configfile as first parameter!')
    exit('1')
path_to_config = argv[1]
data = yaml.safe_load(open(path_to_config))

rospy.loginfo('Creating direction of arrival instance...')

splitter = esiaf_channel_utils.Splitter()

rospy.loginfo('Creating esiaf handler...')
handler = pyesiaf.Esiaf_Handler('esiad_splitter', pyesiaf.NodeDesignation.Other, sys.argv)

rospy.loginfo('Setting up esiaf...')
esiaf_format = esiaf_channel_utils.create_esiaf_audio_format_from_dict(data['esiaf_input']['format'])

esiaf_audio_info = pyesiaf.EsiafAudioTopicInfo()
esiaf_audio_info.topic = data['esiaf_input']['topic']
esiaf_audio_info.allowedFormat = esiaf_format


rospy.loginfo('adding output topics...')
output_topics = []
channels = esiaf_format.channels
esiaf_format.channels = 1

for each in range(channels):
    esiaf_audio_out_info = pyesiaf.EsiafAudioTopicInfo()
    esiaf_audio_out_info.topic = data['esiaf_output_topic_prefix'] + str(each)
    esiaf_audio_out_info.allowedFormat = esiaf_format
    handler.add_output_topic(esiaf_audio_out_info)
    output_topics.append(esiaf_audio_out_info)

rospy.loginfo('adding input topic...')


def input_callback(audio, timeStamps):

    # call dao wrapper
    split = splitter.split(audio)

    # publish output
    for index, topic in enumerate(output_topics):
        handler.publish(topic.topic,
                        split[index],
                        timeStamps)


handler.add_input_topic(esiaf_audio_info, input_callback)
rospy.loginfo('input topic added')
handler.start_esiaf()

rospy.loginfo('Splitter ready!')
rospy.spin()

handler.quit_esiaf()