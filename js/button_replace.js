function button_replace(inid) {
  document.getElementById(inid).innerHTML = '<audio controls><source src=\"' + inid + '\" type="audio/mpeg"></audio>';
  return;
}