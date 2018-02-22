function button_replace(inid) {
  document.getElementById("audiometer").innerHTML = '<audio controls><source src=\"' + inid + '\" type="audio/mpeg"></audio>';
  return;
}
function get_episode_html(episode_id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("audiometer").innerHTML = this.responseText;
            document.getElementById("audioplayer").play();
        }
    };
    xhttp.open("GET", "/episodes/" + episode_id, true);
    xhttp.send();
}
function scroll_to_top() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}