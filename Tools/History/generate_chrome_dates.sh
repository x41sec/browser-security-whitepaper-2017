for a in `find -name "stable-channel-update-for-desktop*"  | grep -v omment ` ; do 
	grep -A1 "'publishdate'" $a ; 
done | grep -v span | cut -d " " -f 2- | awk '{print $2,$1,$3};' | sed 's/,/ /g'
