REPLACE INTO io_point (name,direction, ioType) values("switch.test_start","OUT",'MQTT');

REPLACE INTO io_point (name,direction, ioType) values("switch.test_stop","OUT",'MQTT');

REPLACE INTO io_point (name,direction, ioType) values("switch.dining_room_left","OUT",'MQTT');

REPLACE INTO mqtt (name, command_topic, state_topic,availability_topic) VALUES ('switch.dining_room_left','/home/house/DRLeft/cmnd/power','/home/house/DRLeft/POWER','/home/house/DRLeft/LWT');
REPLACE INTO io_point (name,direction, ioType) values("switch.dining_room_right","OUT",'MQTT');
REPLACE INTO mqtt (name, command_topic, state_topic,availability_topic) VALUES ('switch.dining_room_right','/home/house/DRRight/cmnd/power','/home/house/DRRight/POWER','/home/house/DRRight/LWT');
REPLACE INTO io_point (name,direction, ioType) values("switch.christmas_lights","OUT",'MQTT');
REPLACE INTO mqtt (name, command_topic, state_topic,availability_topic) VALUES ('switch.christmas_lights','/home/house/ChristmasTree/cmnd/power','/home/house/ChristmasTree/POWER','/home/house/ChristmasTree/LWT');
REPLACE INTO io_point (name,direction, ioType) values("switch.penguins","OUT",'MQTT');
REPLACE INTO mqtt (name, command_topic, state_topic,availability_topic) VALUES ('switch.penguins','/home/house/penguins/cmnd/power','/home/house/penguins/POWER','/home/house/penguins/LWT');


REPLACE INTO io_point (name,direction, ioType) values("switch.porch_light","OUT",'MQTT');
REPLACE INTO mqtt (name, command_topic, state_topic,availability_topic) VALUES ('switch.porch_light','/home/outside/PorchLight_1/cmnd/power','/home/outside/PorchLight_1/POWER','/home/outside/PorchLight_1/LWT');
REPLACE INTO io_point (name,direction, ioType) values("switch.back_floodlights","OUT",'MQTT');
REPLACE INTO mqtt (name, command_topic, state_topic,availability_topic) VALUES ('switch.back_floodlights','/home/outside/BackFloodlight/cmnd/power','/home/outside/BackFloodlight/POWER','/home/outside/BackFloodlight/LWT');
REPLACE INTO io_point (name,direction, ioType) values("switch.punch","OUT",'MQTT');
