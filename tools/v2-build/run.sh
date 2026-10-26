set -e
cd /tmp/claude-0/-home-claude/3e881c95-6cf0-56cd-aa41-2012ca221448/scratchpad
node gen.js >/dev/null
python3 buildv2.py
python3 storiesv2.py >/dev/null
python3 v2extra.py
O=/mnt/user-data/outputs/site-v2
# two pages: index.html is the pitch, demo.html is the demo
sed -e 's/index-v2\.html/demo.html/g' -e 's#assets/qr-code.png#assets/qr-demo.png#g' -e 's#<p class="cta-url">goodnight-ai-opal.vercel.app</p>#<p class="cta-url">goodnight-ai-opal.vercel.app/demo</p>#' -e 's#alt="QR code linking to goodnight-ai-opal.vercel.app"#alt="QR code linking to goodnight-ai-opal.vercel.app/demo"#' /tmp/claude-0/-home-claude/3e881c95-6cf0-56cd-aa41-2012ca221448/scratchpad/build/pitch-v2.html > $O/index.html
sed 's/pitch-v2\.html/index.html/g' /tmp/claude-0/-home-claude/3e881c95-6cf0-56cd-aa41-2012ca221448/scratchpad/build/index-v2.html > $O/demo.html
printf '{\n  "cleanUrls": true\n}\n' > $O/vercel.json
rm -f $O/pitch.html
python3 - <<'PY'
O='/mnt/user-data/outputs/site-v2/'
for f,a,b in [('index.html','<title>Goodnight, AI · Pitch v2</title>','<title>Goodnight, AI</title>'),('demo.html','<title>v2 · Goodnight, AI Story Shelf','<title>Goodnight, AI · Demo')]:
    s=open(O+f).read(); s=s.replace(a,b); open(O+f,'w').write(s)
PY

cp $O/index.html $O/demo.html $O/vercel.json /home/claude/gn-repo/
