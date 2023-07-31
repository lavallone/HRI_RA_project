// User defined blocks

Blockly.Blocks['begin'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("begin");
    this.setNextStatement(true, null);
    this.setColour(0);
 this.setTooltip("begin of program");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['end'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("end");
    this.setPreviousStatement(true, null);
    this.setColour(0);
 this.setTooltip("end of program");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['forward'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("img/up.png", 20, 20, "Forward"));
    this.appendValueInput("steps")
        .setCheck("Number")
        .appendField("forward");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
 this.setTooltip("robot moves forward");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['backward'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("img/down.png", 20, 20, "Backward"));
    this.appendValueInput("steps")
        .setCheck("Number")
        .appendField("backward");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
 this.setTooltip("robot moves backward");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['left'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("img/rotleft.png", 20, 20, "Left"));
    this.appendValueInput("steps")
        .setCheck("Number")
        .appendField("left");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
 this.setTooltip("robot turns left");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['right'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("img/rotright.png", 20, 20, "Right"));
    this.appendValueInput("steps")
        .setCheck("Number")
        .appendField("right");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
 this.setTooltip("robot turns right");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['wait'] = {
  init: function() {
    /*this.appendDummyInput().appendField(new Blockly.FieldImage("img/rotright.png", 20, 20, "Wait"));*/
    this.appendValueInput("seconds")
        .setCheck("Number")
        .appendField("wait");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
 this.setTooltip("robot waits [seconds]");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['turn'] = {
  init: function() {
    /*this.appendDummyInput().appendField(new Blockly.FieldImage("img/rotright.png", 20, 20, "Turn"));*/
    this.appendValueInput("degrees")
        .setCheck("Number")
        .appendField("turn");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
 this.setTooltip("robot turns [angle in degrees]");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['setSpeed'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("setSpeed");
    this.appendValueInput("tv")
        .setCheck("Number")
        .appendField("tv");
    this.appendValueInput("rv")
        .setCheck("Number")
        .appendField("rv");
    this.appendValueInput("time")
        .setCheck("Number")
        .appendField("time");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
 this.setTooltip("robot turns [angle in degrees]");
 this.setHelpUrl("");
  }
};


Blockly.Blocks['get_pose'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("get_pose()");
    this.setOutput(true, null);
    this.setColour(0);
 this.setTooltip("returns the pose of the robot [x,y,theta]");
 this.setHelpUrl("");
  }
};


Blockly.Blocks['obstacle_distance'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("obstacle_distance")
        .appendField(new Blockly.FieldDropdown([["front","OPTIONFRONT"], ["left","OPTIONLEFT"], ["right","OPTIONRIGHT"]]), "direction");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setColour(0);
 this.setTooltip("distance of obstable");
 this.setHelpUrl("");
  }
};


Blockly.Blocks['distance'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("distance");
    this.appendValueInput("P1")
        .setCheck(null);
    this.appendValueInput("P2")
        .setCheck(null);
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setColour(0);
 this.setTooltip("returns distance between two poses");
 this.setHelpUrl("");
  }
};


