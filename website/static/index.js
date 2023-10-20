function deleteAd(adId) { //takes the note id and sends a post request to delete-ad
  fetch("/delete-ad", {
    method: "POST",
    body: JSON.stringify({ adId: adId }), //turns it  into a string
  }).then((_res) => {
    window.location.href = "/"; //when it get a response from delete-note it loads home page
  });
}
