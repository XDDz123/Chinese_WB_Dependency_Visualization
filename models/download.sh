wget "https://zenodo.org/records/15096936/files/UD_Chinese-GSDLTP.tar.gz"
wget "https://zenodo.org/records/15096936/files/UD_Chinese-GSDPenn.tar.gz"
wget "https://zenodo.org/records/15096936/files/UD_Chinese-GSDPKU.tar.gz"
wget "https://zenodo.org/records/15096936/files/UD_Chinese-GSDSimp.tar.gz"
wget "https://zenodo.org/records/15096936/files/UD_Chinese-GSDspaCy.tar.gz"

for i in *.gz
do
	echo $i
	tar xvfz $i
done
