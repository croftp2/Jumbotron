function button_replace(inid) {
  document.getElementById("audiometer").innerHTML = '<audio controls><source src=\"' + inid + '\" type="audio/mpeg"></audio>';
  // document.getElementById("audiometer").innerHTML = '<source src=\"' + inid + '\" type="audio/mpeg">';
  return;
}
function get_episode_html(episode_id) {
    console.log("Got request for " + episode_id)
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log("HERE")
            document.getElementById("audiometer").innerHTML = this.responseText;
        }
        console.log("ready state change to " + this.readyState)
    };
    xhttp.open("GET", "episodes/" + episode_id, true);
    xhttp.send();
}