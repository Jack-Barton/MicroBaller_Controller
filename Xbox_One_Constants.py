"""
Controller value list index for specified Xbox one controller outputs (index in the message list)
Zero state for the array/list = [128, 128, 128, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Each variable below is assigned its specific index in the message list
"""
_Axis_Left_LR           = 0     # Values 0-255
_Axis_Left_Axis_UD      = 1     # Values 0-255
_Axis_Right_Axis_LR     = 2     # Values 0-255
_Axis_Right_Axis_UD     = 3     # Values 0-255
_Trigger_Left           = 4     # Values 0-255
_Trigger_Right          = 5     # Values 0-255
_Button_A               = 6     # Values 0 or 1
_Button_B               = 7     # Values 0 or 1
_Button_X               = 8     # Values 0 or 1
_Button_Y               = 9     # Values 0 or 1
_Bumper_Left            = 10    # Values 0 or 1
_Bumper_Right           = 11    # Values 0 or 1
_Button_Menu            = 12    # Values 0 or 1
_Button_Start           = 13    # Values 0 or 1
_Button_Axis_Left       = 14    # Values 0 or 1
_Button_Axis_Right      = 15    # Values 0 or 1
_Unknown_1              = 16    # N/A
_Unknown_2              = 17    # N/A
_Unknown_3              = 18    # N/A
_Unknown_4              = 19    # N/A
_Unknown_5              = 20    # N/A
_Unknown_6              = 21    # N/A

"""
Button Assignment (Assign the action of each button/joystick/trigger)
"""
_Disconnect             = _Button_Start     # Controller start button will stop the program
