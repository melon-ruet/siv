1. Install termcolor using pip
sudo apt-get install python-pip
sudo pip install termcolor

2. Initialization mode command
python siv.py -i -D /path/to/monitor/dir -V /path/to/verification.txt -R /path/to/init_report.txt -H sha1

3. Verification mode command
python siv.py -v -D /path/to/monitor/dir -V /path/to/verification.txt -R /path/to/ver_report.txt

4. For help mode:
python siv.py -h
