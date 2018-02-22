function button_replace(inid) {
  document.getElementById("audiometer").innerHTML = '<audio controls><source src=\"' + inid + '\" type="audio/mpeg"></audio>';
  // document.getElementById("audiometer").innerHTML = '<source src=\"' + inid + '\" type="audio/mpeg">';
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