mkdir -p ../installer/usr/share/calculator
cp  math_lib.py ../installer/usr/share/calculator/math_lib.py
cp  extended_math_lib.py ../installer/usr/share/calculator/extended_math_lib.py
cp  gui.py ../installer/usr/share/calculator/gui.py
chmod +x ../installer/usr/share/calculator/gui.py
cp  stddev.py ../installer/usr/share/calculator/stddev.py
chmod +x ../installer/usr/share/calculator/stddev.py
mkdir -p ../installer/usr/share/applications
cp  calculator.desktop ../installer/usr/share/applications/calculator.desktop
chmod +x ../installer/usr/share/applications/calculator.desktop
mkdir -p ../installer/usr/share/icons
cp  calculator.xpm ../installer/usr/share/icons/calculator.xpm
mkdir -p ../installer/usr/local/bin
sudo ln -sf /usr/share/calculator/gui.py ../installer/usr/local/bin/ivs-calculator
sudo ln -sf /usr/share/calculator/stddev.py ../installer/usr/local/bin/ivs-deviation
mkdir ../installer/tmp
cp dependencies.txt ../installer/tmp/dependencies.txt
chmod +x ../installer/DEBIAN/postinst
export PATH=$PATH:/usr/local/bin
source ~/.bashrc
dpkg-deb --build ../installer/ ../installer/calculator_installer.deb
