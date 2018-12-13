function create_add_podcast_button(plus){
  document.getElementById("add_podcasts_div").innerHTML = `
  <h3>Add a podcasts via RSS feed</h3>
  <input type="text" name="new_rss" id="new_rss" default="http link here...">
  <button onmouseup="submit_new_rss();" type="submit">Submit</button>
  <p>` + plus + `</p>
  <hr>
`;
}
function submit_new_rss(){
  new_rss_link = document.getElementById("new_rss").value;
  document.getElementById("add_podcasts_div").innerHTML = `
  <h3>Submitted!</h3>
  <hr>
`;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      create_add_podcast_button("Podcast '" + this.responseText + "' added successfully");
    } else if (this.readyState != 4 && this.readyState != 0) {
      document.getElementById("add_podcasts_div").innerHTML = `
  <h3>Processing...</h3>
  <hr>
`;
    } else if (this.readyState == 4 && this.status == 409) {//Duplicate
      create_add_podcast_button("That podcast has already been added")
    } else if (this.readyState == 4) {//unsuccessfull addition
      create_add_podcast_button("Failed to add podcast")
    }


  };
  xhttp.open("POST", "/new_rss/", true);
  xhttp.send(new_rss_link);


}