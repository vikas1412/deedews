 function post_tab(){
     posttab = document.getElementById('posts');
     posttab.style.display = 'none';

     postimage = document.getElementById('images');
     postimage.style.display = 'block';
     console.log("Clicked on Container");
 }

 function changeTabs(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();


function readURL_pic(input) {
    if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#post_image')
                    .attr('src', e.target.result)
                    .height(430);
            };

            reader.readAsDataURL(input.files[0]);
        }
}