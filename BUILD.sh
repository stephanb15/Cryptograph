
#This file is created by author: Stephan Bornberg

#Download Python3 (debian assumed)

sudo apt-get update
sudo apt-get install python3

#Download dependencies

#pip install pyinstaller
#pip3 install pyinstaller

pip3 install numpy
pip install numpy

#copy project into linux file system

srcDIR=$(pwd)
cp -r "$srcDIR" ~/.local/share

#open linux file structure where the project is copyed to and make cryptograph executable

sudo chmod +x ~/.local/share/Cryptograph/cryptograph.py
sudo chmod +w ~/.local/share/Cryptograph

#Create a .desktop file, so you will see the application in the applicaiton menue

cd ~/.local/share/applications

echo "[Desktop Entry]" > Cryptograph.desktop
echo "Encoding=UTF-8" >> Cryptograph.desktop
echo "Version=1.0" >> Cryptograph.desktop
echo "Type=Application" >> Cryptograph.desktop
echo "Terminal=false" >> Cryptograph.desktop
Exec=~/.local/share/Cryptograph/cryptograph.py
Icon=~/.local/share/Cryptograph/Icons/icon.png
echo "Exec=${Exec}" >> Cryptograph.desktop
echo "Icon=${Icon}" >> Cryptograph.desktop
echo "Name=Cryptograph" >> Cryptograph.desktop
echo "Type=Application" >> Cryptograph.desktop

# make .desktop file executable (otherwise linux will not take care of it)

chmod +x ~/.local/share/applications/Cryptograph.desktop
