    var x = document.createElement("IFRAME");
    x.setAttribute("src", "https://www.twitter.com");
    document.body.appendChild(x);

    var x = document.createElement("IFRAME");
    x.setAttribute("width", "800");x.setAttribute("height", "600");
    x.setAttribute("src", "data:text/plain,<script>alert(10)</script>");
    document.body.appendChild(x);

