#Download Python3 (debian assumed)

sudo apt-get update
sudo apt-get install python3

#Download dependencies

#pip install pyinstaller
#pip3 install pyinstaller

#open linux file structure where the project should be made

srcDIR=$(pwd)
cp -r "$srcDIR" ~/.local/share
cd ~/.local/share/Cryptograph

cp ~/.local/share/Cryptograph/Cryptograph.desktop ~/.local/share/applications

