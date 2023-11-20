# Motion Activated Camera

This project was inspired by a neighborhood cat that would come into our house through our pet door and make himself at home. We weren't sure when he would come in. We'd always just find him there. I built this motion-sensing camera and set it up next to my pet door so I could find out when the little guy was getting into the house.

## Notes for future me:

### config.py:

>**`FILENAME_PREFIX`**
>
>>This prefix will be added to the beginning of each file  
>>- **NOTE:** that without a prefix, the filename will begin with a '-'.
>>
>>`{FILENAME_PREFIX}`-000000-[hh.mm]
>
>---
>
>**`SAVE_DIRECTORY_PATH`**
>
>>- example: "/home/meowth/motion_camera/recordings"  
>>- **NOTE:** that any subdirectories inside of the project folder (such as 'recordings' above) MUST be created before running the program. The program will automatically create a directory for the videos recorded during a particular day, however that is the ONLY directory it will create.
>
>---
>
>**`DIRECTORY_NAME_PREFIX`**
>
>>This is the name of the directiory where the video files will be stored.
>>
>>`{DIRECTORY_NAME_PREFIX}`MM.DD.YYYY
>
>---
>
>**`LED_INDICATORS`**
>
>This turns the LED indicators on or off.
>
>`True`: The LED indicators will function normally. This is useful for testing when away from a monitor/keyboard. Also, when recording people, this lets others know that the device is on and/or recording.
>
>`False`: The LED indicators will be disabled. This is useful for recording animals, or other situations where you would not want to it to be immediately obvious that the camera is doing anything.
>
### preview.py

This file was used during testing. It starts the camera with a preview window in order to verify the camera is working, and to test the camera under various conditions.