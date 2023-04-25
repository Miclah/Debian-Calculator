chmod +x ../installer/DEBIAN/postinst
mkdir -p ../installer/usr/share/calculator
cp  math_lib.py ../installer/usr/share/calculator/math_lib.py
cp  extended_math_lib.py ../installer/usr/share/calculator/extended_math_lib.py
cp  gui.py ../installer/usr/share/calculator/gui.py
chmod +x ../installer/usr/share/calculator/gui.py
mkdir -p ../installer/usr/share/applications
cp  calculator.desktop ../installer/usr/share/applications/calculator.desktop
chmod +x ../installer/usr/share/applications/calculator.desktop
mkdir -p ../installer/usr/share/icons
cp  calculator.xpm ../installer/usr/share/icons/calculator.xpm
mkdir -p ../installer/usr/local/bin
ln -sf /usr/share/calculator/gui.py ../installer/usr/local/bin/ivs-calculator
mkdir ../installer/tmp
cp dependencies.txt ../installer/tmp/dependencies.txt
export PATH=$PATH:/usr/local/bin
source ~/.bashrc
dpkg-deb --build ../installer/ ../installer/calculator_installer.deb
