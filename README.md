# tinGUI
WIP a text editor written in python

### debian based distros dependecies
```bash
sudo apt install -y python3 python3-pip python3-tk idle3 curl
```

run without downloading the python file
```bash
curl -s https://raw.githubusercontent.com/BeanGreen247/tinGUI/main/tinGUI/tinGUI.py | python3 -s &
```

### windows
Download the latest version of curl

https://curl.se/windows/

next extract it into your C: drive like so

`C:\curl-8.0.1_7-win64-mingw`

next locate the `bin` folder

`C:\curl-8.0.1_7-win64-mingw\bin`

So copy the location.

Next Search for `view advanced system settings` a window should open upon selecting it.

In the window find `Environment Variables...` once there you should see `User variables for ...` and `System Variables`

In both you want to find Path so select once and click on `Edit...` a new window should show up so click on `New` and paste in the path to the curl bin folder `C:\curl-8.0.1_7-win64-mingw\bin`

Do the same for both `User variables for ...` and `System Variables`.

Next open Powershell and type in the following

***Note: make sure that your python install is also in the Path for both `User variables for ...` and `System Variables`.***

```powershell
curl.exe https://raw.githubusercontent.com/BeanGreen247/tinGUI/main/tinGUI/tinGUI.py | python.exe
```
This should open the text editor without having to download it.

### TODO
* ~~Loading of files~~
* ~~Saving files~~
  * ~~Save button with no dialog~~
  * ~~Save As button with dialog~~
* Programming Language syntax support
  * ~~Python~~
  * Bash
  * Java
  * C#
> more languages will be added as time goes on...

### Issues/Bug reporting
If you encounter a bug/problem, please report it here, thx

https://github.com/BeanGreen247/tinGUI/issues

BeanGreen247, 2023
