# ignite_poster

Uses standard python libraries. Should not require any additional pip libraries.
To make this work on multiple platforms and operating systems edit the config to ensure slashes are the correct direction.

If you want to add fonts to the poster download the fonts and add them to the resources directory. Then update the config for the new font.

Make sure images are saved in the format "First Name.[image extension]"

You can change the default images in the upper left and ad lower right hand corner of the header by changing the files in the resources folder and then updating the names of the files in the config.

Change the overall size of the document in the config with the poster section. The value for _height and _width are ignored but should be good places to start with the heigh and width settings.

If you run the script it will overwrite whatever is currently saved in the file_name section of the config. You will not get a request to confirm or anything. It will just overwrite. 

