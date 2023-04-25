chmod +x ../installer/DEBIAN/postinst
mkdir -p ../installer/usr/share/deviation
cp  math_lib.py ../installer/usr/share/deviation/math_lib.py
cp  extended_math_lib.py ../installer/usr/share/deviation/extended_math_lib.py
cp  stddev.py ../installer/usr/share/deviation/stddev.py
chmod +x ../installer/usr/share/deviation/stddev.py
mkdir -p ../installer/usr/local/bin
sudo ln -sf /usr/share/deviation/stddev.py ../installer/usr/local/bin/ivs-deviation
mkdir ../installer/tmp
cp dependencies.txt ../installer/tmp/dependencies.txt
export PATH=$PATH:/usr/local/bin
source ~/.bashrc
dpkg-deb --build ../installer/ ../installer/deviation_installer.deb
